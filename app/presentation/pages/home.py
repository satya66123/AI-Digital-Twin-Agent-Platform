
import streamlit as st

from app.application import ApplicationContainer
from app.domain.entities.memory_type import MemoryType
from app.domain.entities.conversation_status import ConversationStatus


def render(container: ApplicationContainer) -> None:
    st.title("🤖 AI Digital Twin Agent Platform")

    st.markdown(
        """
        Welcome to the AI Digital Twin Agent Platform.

        Manage knowledge, memories, and AI-powered intelligence
        using multiple AI providers and models.
        """
    )

    # ------------------------------------------
    # AI Provider and Model Selection
    # ------------------------------------------

    st.header("🤖 AI Configuration")

    service = container.create_provider_model_service()
    providers = service.get_providers()

    if not providers:
        st.warning("No AI providers are currently available.")
        return

    provider = st.selectbox(
        "Select Provider",
        providers,
        key="selected_provider",
    )

    models = service.get_models(provider)

    model_names = [model.name for model in models]

    if model_names:
        selected_model = st.selectbox(
            "Select Model",
            model_names,
            key="selected_model",
        )
    else:
        selected_model = None
        st.warning("No models available for this provider.")

    st.divider()

    # ------------------------------------------
    # Existing Knowledge Agent
    # ------------------------------------------

    knowledge_agent = container.create_knowledge_agent()

    st.header("📚 Knowledge Management")

    upload_tab, search_tab = st.tabs(
        [
            "📤 Document Ingestion",
            "🔎 Knowledge Search",
        ]
    )

    # ------------------------------------------
    # Document Ingestion
    # ------------------------------------------

    with upload_tab:
        st.subheader("Upload Knowledge Documents")

        st.caption(
            "Supported formats: PDF, DOCX, TXT, MD, CSV"
        )

        with st.form("knowledge_upload_form"):
            uploaded_file = st.file_uploader(
                "Choose a document",
                type=["pdf", "docx", "txt", "md", "csv"],
            )

            author = st.text_input(
                "Document Author",
                placeholder="Optional",
            )

            source_url = st.text_input(
                "Source URL",
                placeholder="Optional",
            )

            submit_upload = st.form_submit_button(
                "Ingest Document",
                type="primary",
            )

        if submit_upload:
            if uploaded_file is None:
                st.warning("Please select a document first.")
            else:
                try:
                    with st.spinner(
                        "Processing and ingesting document..."
                    ):
                        result = knowledge_agent.ingest_document(
                            filename=uploaded_file.name,
                            content=uploaded_file.getvalue(),
                            author=author,
                            source_url=source_url,
                        )

                    st.success("Document ingested successfully!")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "File Size",
                        f"{result.file_size / 1024:.2f} KB",
                    )

                    col2.metric(
                        "Knowledge Chunks",
                        result.chunk_count,
                    )

                    col3.metric(
                        "Extracted Characters",
                        result.extracted_character_count,
                    )

                    st.write("**Filename:**", result.filename)
                    st.write(
                        "**Knowledge Item ID:**",
                        result.knowledge_item_id,
                    )
                    st.write("**Source ID:**", result.source_id)

                except Exception as exc:
                    st.error(f"Document ingestion failed: {exc}")

    # ------------------------------------------
    # Knowledge Search
    # ------------------------------------------

    with search_tab:
        st.subheader("Search Your Knowledge Base")

        with st.form("knowledge_search_form"):
            query = st.text_input(
                "Enter your search query",
                placeholder="Example: Explain artificial intelligence",
            )

            result_limit = st.slider(
                "Maximum Results",
                min_value=1,
                max_value=20,
                value=5,
            )

            submit_search = st.form_submit_button(
                "Search Knowledge",
                type="primary",
            )

        if submit_search:
            if not query.strip():
                st.warning("Please enter a search query.")
            else:
                try:
                    with st.spinner("Searching knowledge..."):
                        context = knowledge_agent.retrieve_context(
                            query=query,
                            limit=result_limit,
                        )

                    if context.result_count == 0:
                        st.info("No relevant knowledge found.")
                    else:
                        st.success(
                            f"Found {context.result_count} relevant chunks."
                        )

                        st.subheader("Search Results")

                        for index, result in enumerate(
                            context.results,
                            start=1,
                        ):
                            with st.expander(
                                f"Result {index} | "
                                f"Score: {result.relevance_score}"
                            ):
                                st.write(result.content)
                                st.caption(
                                    f"Knowledge Item ID: "
                                    f"{result.knowledge_item_id}"
                                )
                                st.caption(f"Chunk ID: {result.chunk_id}")
                                st.caption(
                                    f"Chunk Index: {result.chunk_index}"
                                )

                        st.subheader("Retrieved Context")

                        st.text_area(
                            "Context prepared for the Digital Twin",
                            value=context.context_text,
                            height=250,
                            disabled=True,
                        )

                except Exception as exc:
                    st.error(f"Knowledge search failed: {exc}")

    st.divider()

    # ==========================================
    # Phase 2: Memory Management
    # ==========================================

    st.header("🧠 Memory Management")

    memory_service = container.create_memory_service()

    memory_agent = None

    if selected_model:
        memory_agent = container.create_memory_agent(provider)

    save_tab, view_tab, memory_search_tab = st.tabs(
        [
            "💾 Save Memory",
            "📖 View Memories",
            "🔎 Search Memories",
        ]
    )

    # ------------------------------------------
    # Save Memory
    # ------------------------------------------

    with save_tab:
        st.subheader("Create Digital Twin Memory")

        with st.form("memory_creation_form"):
            memory_content = st.text_area(
                "Memory Content",
                placeholder="Enter information to remember...",
                height=120,
            )

            memory_type = st.selectbox(
                "Memory Type",
                options=list(MemoryType),
                format_func=lambda item: item.value.replace("_", " ").title(),
            )

            submit_memory = st.form_submit_button(
                "Save Memory",
                type="primary",
            )

        if submit_memory:
            if not memory_content.strip():
                st.warning("Please enter memory content.")
            else:
                try:
                    with st.spinner("Saving memory..."):
                        memory = memory_service.create_memory(
                            content=memory_content,
                            memory_type=memory_type,
                        )

                    st.success("Memory saved successfully!")
                    st.write("**Memory ID:**", memory.memory_id)
                    st.write("**Memory Type:**", memory.memory_type.value)

                except Exception as exc:
                    st.error(f"Memory creation failed: {exc}")

    # ------------------------------------------
    # View Memories
    # ------------------------------------------

    with view_tab:
        st.subheader("Stored Memories")

        selected_memory_type = st.selectbox(
            "Filter by Memory Type",
            options=["All"] + list(MemoryType),
            format_func=lambda item: (
                item if item == "All"
                else item.value.replace("_", " ").title()
            ),
            key="memory_type_filter",
        )

        if selected_memory_type == "All":
            memories = memory_service.get_all_memories()
        else:
            memories = memory_service.get_memories_by_type(
                selected_memory_type
            )

        st.metric("Total Memories", len(memories))

        if not memories:
            st.info("No memories found.")
        else:
            for memory in memories:
                with st.expander(
                    f"{memory.memory_type.value.title()} | "
                    f"{memory.content[:60]}"
                ):
                    st.write(memory.content)
                    st.caption(f"Memory ID: {memory.memory_id}")
                    st.caption(
                        f"Created: {memory.created_at.isoformat()}"
                    )

                    if st.button(
                        "Delete Memory",
                        key=f"delete_memory_{memory.memory_id}",
                    ):
                        if memory_service.delete_memory(
                            memory.memory_id
                        ):
                            st.success("Memory deleted.")
                            st.rerun()

        st.divider()

        st.subheader("Memory Consolidation")

        if st.button(
            "Consolidate Short-Term Memories",
            key="consolidate_memories",
        ):
            try:
                with st.spinner("Consolidating memories..."):
                    count = memory_service.consolidate_short_term_memories()

                st.success(
                    f"Consolidated {count} short-term memories."
                )
                st.rerun()

            except Exception as exc:
                st.error(f"Memory consolidation failed: {exc}")

    # ------------------------------------------
    # Search Memories
    # ------------------------------------------

    with memory_search_tab:
        st.subheader("Search Stored Memories")

        with st.form("memory_search_form"):
            memory_query = st.text_input(
                "Search memories",
                placeholder="Example: Python development",
            )

            submit_memory_search = st.form_submit_button(
                "Search Memories",
                type="primary",
            )

        if submit_memory_search:
            if not memory_query.strip():
                st.warning("Please enter a search query.")
            else:
                try:
                    results = memory_service.search_memories(
                        memory_query
                    )

                    if not results:
                        st.info("No matching memories found.")
                    else:
                        st.success(
                            f"Found {len(results)} matching memories."
                        )

                        for memory in results:
                            with st.expander(memory.content[:80]):
                                st.write(memory.content)
                                st.caption(
                                    f"Type: {memory.memory_type.value}"
                                )
                                st.caption(
                                    f"Memory ID: {memory.memory_id}"
                                )

                except Exception as exc:
                    st.error(f"Memory search failed: {exc}")

    st.divider()

    # ==========================================
    # Phase 2: Digital Twin Intelligence
    # ==========================================

    st.header("✨ Digital Twin Intelligence")

    st.caption(
        "Generate AI responses using your stored knowledge and memories."
    )

    with st.form("digital_twin_form"):
        user_query = st.text_area(
            "Ask your Digital Twin",
            placeholder="Ask a question about your knowledge or memories...",
            height=120,
        )

        submit_question = st.form_submit_button(
            "Generate AI Response",
            type="primary",
            disabled=not bool(selected_model),
        )

    if submit_question:
        if not user_query.strip():
            st.warning("Please enter a question.")
        elif memory_agent is None:
            st.warning("Please select an AI model first.")
        else:
            try:
                with st.spinner(
                    f"Generating response using {provider}..."
                ):
                    result = memory_agent.answer(
                        query=user_query,
                        model=selected_model,
                    )

                st.subheader("Digital Twin Response")
                st.write(result.response)

                with st.expander("View Retrieved Knowledge and Memory"):
                    st.write("**Knowledge Context**")
                    st.write(result.context.knowledge_context or "No knowledge found.")

                    st.write("**Memory Context**")
                    st.write(result.context.memory_context or "No memories found.")

                    st.write(
                        "**Retrieved Memories:**",
                        result.context.total_memories,
                    )

            except Exception as exc:
                st.error(f"AI response generation failed: {exc}")

    st.divider()


    # ==========================================
    # Phase 3: Digital Twin Conversation
    # ==========================================

    st.divider()
    st.header("💬 Digital Twin Conversation")

    st.caption(
        "Have continuous conversations with your Digital Twin "
        "using your knowledge base and stored memories."
    )

    conversation_service = container.create_conversation_service()

    # ------------------------------------------
    # Conversation Creation
    # ------------------------------------------

    st.subheader("Conversation Management")

    new_title = st.text_input(
        "New Conversation Title",
        value="New Digital Twin Conversation",
        key="new_conversation_title",
    )

    if st.button(
        "➕ Create New Conversation",
        key="create_digital_twin_conversation",
        disabled=not bool(new_title.strip()),
    ):
        try:
            conversation = conversation_service.create_conversation(
                title=new_title.strip()
            )

            conversation_id = str(conversation.conversation_id)

            st.session_state["active_conversation_id"] = conversation_id
            st.session_state["conversation_selector"] = conversation_id

            st.success("Conversation created successfully!")
            st.rerun()

        except Exception as exc:
            st.error(f"Conversation creation failed: {exc}")

    # ------------------------------------------
    # Load Existing Conversations
    # ------------------------------------------

    conversations = conversation_service.get_all_conversations()

    conversation_map = {
        str(item.conversation_id): item
        for item in conversations
    }

    if not conversations:
        st.info("Create a conversation to start chatting with your Digital Twin.")

    else:
        conversation_ids = list(conversation_map.keys())

        active_id = st.session_state.get("active_conversation_id")

        if active_id not in conversation_ids:
            active_id = conversation_ids[0]
            st.session_state["active_conversation_id"] = active_id

        if st.session_state.get("conversation_selector") not in conversation_ids:
            st.session_state["conversation_selector"] = active_id

        selected_conversation_id = st.selectbox(
            "Select Conversation",
            options=conversation_ids,
            format_func=lambda item: (
                f"{conversation_map[item].title} "
                f"({conversation_map[item].status.value})"
            ),
            key="conversation_selector",
        )

        st.session_state["active_conversation_id"] = (
            selected_conversation_id
        )

        selected_conversation = conversation_map[
            selected_conversation_id
        ]

        st.caption(
            f"Conversation ID: {selected_conversation_id}"
        )

        # ------------------------------------------
        # Conversation Actions
        # ------------------------------------------

        action_col1, action_col2 = st.columns(2)

        if selected_conversation.status == ConversationStatus.ACTIVE:

            with action_col1:
                if st.button(
                    "📦 Archive Conversation",
                    key=f"archive_{selected_conversation_id}",
                ):
                    try:
                        conversation_service.archive_conversation(
                            selected_conversation.conversation_id
                        )
                        st.success("Conversation archived.")
                        st.rerun()

                    except Exception as exc:
                        st.error(f"Archiving failed: {exc}")

        with action_col2:
            if st.button(
                "🗑️ Delete Conversation",
                key=f"delete_conversation_{selected_conversation_id}",
            ):
                try:
                    conversation_service.delete_conversation(
                        selected_conversation.conversation_id
                    )

                    st.session_state.pop("active_conversation_id", None)
                    st.session_state.pop("conversation_selector", None)

                    st.success("Conversation deleted.")
                    st.rerun()

                except Exception as exc:
                    st.error(f"Conversation deletion failed: {exc}")

        st.divider()

        # ------------------------------------------
        # Conversation History
        # ------------------------------------------

        st.subheader("Chat History")

        conversation_history = conversation_service.get_messages(
            selected_conversation.conversation_id
        )

        if not conversation_history:
            st.info("No messages yet. Start your conversation below.")

        for chat_message in conversation_history:
            role = chat_message.role.value

            if role not in ("user", "assistant"):
                continue

            with st.chat_message(role):
                st.markdown(chat_message.content)

        # ------------------------------------------
        # Multi-turn Conversation
        # ------------------------------------------

        if selected_conversation.status == ConversationStatus.ACTIVE:

            if not selected_model:
                st.warning("Select an AI provider and model to continue.")

            else:
                chat_prompt = st.chat_input(
                    "Message your Digital Twin...",
                    key=f"chat_input_{selected_conversation_id}",
                    disabled=not bool(selected_model),
                )

                if chat_prompt:

                    try:
                        interaction_agent = (
                            container.create_digital_twin_interaction_agent(
                                provider_name=provider,
                                history_limit=10,
                            )
                        )

                        with st.chat_message("user"):
                            st.markdown(chat_prompt)

                        with st.spinner(
                            f"Digital Twin is responding using {provider}..."
                        ):
                            result = interaction_agent.send_message(
                                conversation_id=(
                                    selected_conversation.conversation_id
                                ),
                                message=chat_prompt,
                                model=selected_model,
                            )

                        with st.chat_message("assistant"):
                            st.markdown(result.response)

                        st.rerun()

                    except Exception as exc:
                        st.error(
                            f"Digital Twin conversation failed: {exc}"
                        )

        else:
            st.info(
                "This conversation is archived. "
                "Create a new conversation to continue chatting."
            )


    st.caption(
        "AI Digital Twin Agent Platform | "
        "Knowledge Management | Intelligence & Memory"
    )
