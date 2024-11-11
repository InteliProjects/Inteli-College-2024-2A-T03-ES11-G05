import streamlit as st
import pandas as pd
import requests

# Configurações iniciais
st.title("Ingests")
BASE_URL = "http://0.0.0.0:5500"

# Opção de selecionar a funcionalidade
options = st.selectbox("Select an option", ["Health", "Ingest", "Visualize"])
st.write("Selected option: ", options)

if options == "Health":
    with st.spinner("Checking health..."):
        try:
            # Requisição GET
            st.write(f"Sending request to {BASE_URL}/health")
            response = requests.get(f"{BASE_URL}/health")
            response.raise_for_status()  # Lança uma exceção se o status não for 2xx
            data = response.json()
            st.success("Health check passed!")
            st.write("Response data:", data)
        except requests.exceptions.RequestException as e:
            st.error(f"Error during health check: {e}")
            st.write(f"Exception: {e}")

if options == "Ingest":
    # Upload de múltiplos arquivos CSV
    files = st.file_uploader(
        "Choose .csv files", type="csv", accept_multiple_files=True)

    if files:
        st.write("Uploaded files:")
        for idx, file in enumerate(files, start=1):
            st.write(f"{idx}. {file.name}")

    # Botão para enviar
    if st.button("Ingest"):
        if files:
            with st.spinner("Ingesting files..."):
                # Preparando os dados do form
                files_data = [
                    ("files", (file.name, file.getvalue(), "text/csv")) for file in files
                ]

                try:
                    # Requisição POST
                    st.write(f"Sending request to {BASE_URL}/ingest/")
                    response = requests.post(
                        f"{BASE_URL}/ingest/",
                        files=files_data,
                    )
                    response.raise_for_status()  # Lança uma exceção se o status não for 2xx
                    response_data = response.json()
                    st.success("Files ingested successfully!")
                    st.write("Response data:", response_data)

                except requests.exceptions.RequestException as e:
                    st.error(f"Error during ingestion: {e}")
                    st.write(f"Exception: {e}")
        else:
            st.warning("Please upload files.")

if options == "Visualize":
    tag = st.text_input("Tag")

    if st.button("Visualize"):
        if tag:
            with st.spinner("Retrieving data..."):
                try:
                    response = requests.get(
                        f"{BASE_URL}/ingest/visualize/{tag}")
                    response.raise_for_status()  # Lança uma exceção se o status não for 2xx
                    response_data = response.json()
                    st.success("Data retrieved successfully!")
                    st.write("Response data:", response_data)

                    # Convert the data to a DataFrame
                    data = response_data.get("data", [])
                    if data:
                        # Flatten the 'dado_linha' JSON into the main DataFrame
                        df = pd.json_normalize(data, sep='_')
                        st.dataframe(df)
                    else:
                        st.warning("No data found for the given tag.")

                except requests.exceptions.RequestException as e:
                    st.error(f"Error retrieving data: {e}")
                    st.write(f"Exception: {e}")
        else:
            st.warning("Please enter a tag.")
