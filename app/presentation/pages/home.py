
import streamlit as st

from app.application import ApplicationContainer


def render(container: ApplicationContainer) -> None:
    st.title("🤖 AI Digital Twin Agent Platform")

    st.markdown(
        """
        Welcome to the AI Digital Twin Agent Platform.

        The platform supports multiple AI providers, models,
        and personalized knowledge management.
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

    model_names = [
        model.name
        for model in models
    ]

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
    # Knowledge Agent
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

                    st.success(
                        "Document ingested successfully!"
                    )

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

                    st.write(
                        "**Filename:**",
                        result.filename,
                    )

                    st.write(
                        "**Knowledge Item ID:**",
                        result.knowledge_item_id,
                    )

                    st.write(
                        "**Source ID:**",
                        result.source_id,
                    )

                except Exception as exc:
                    st.error(
                        f"Document ingestion failed: {exc}"
                    )

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
                        st.info(
                            "No relevant knowledge found."
                        )

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

                                st.caption(
                                    f"Chunk ID: {result.chunk_id}"
                                )

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

                        st.caption(
                            "This context is ready for integration "
                            "with the Digital Twin interaction workflow."
                        )

                except Exception as exc:
                    st.error(
                        f"Knowledge search failed: {exc}"
                    )

    st.divider()

    st.caption(
        "AI Digital Twin Agent Platform | "
        "Knowledge Management"
    )
