import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="MediGrid AI",
    page_icon="💊",
    layout="wide"
)


st.title("💊 MediGrid AI")
st.write("Your Personal Prescription Helper")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Prescription",
    "📚 History",
    "📍 Location & Pharmacy",
    "⚠️ Warnings",
    "🤖 Chatbot"
])


# =========================================================
# PRESCRIPTION
# =========================================================

with tab1:

    st.header("📋 Prescription")

    uploaded_file = st.file_uploader(
        "Upload Prescription",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        st.success("Prescription uploaded successfully!")

        st.image(
            uploaded_file,
            caption="Prescription",
            width=500
        )

        if st.button("🔍 Analyze Prescription"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/read_prescription",
                    files=files
                )

                if response.status_code == 200:

                    result = response.json()

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.session_state["prescription"] = result

                else:

                    st.error(
                        f"FastAPI Error: {response.status_code}"
                    )

                    st.code(response.text)

            except Exception as e:

                st.error(str(e))


    if "prescription" in st.session_state:

        data = st.session_state["prescription"]

        st.subheader("👤 Patient Details")

        st.write(
            "Patient Name:",
            data.get("patient_name", "Not available")
        )

        st.write(
            "Doctor Name:",
            data.get("doctor_name", "Not available")
        )

        st.subheader("💊 Medicines")

        medicines = data.get("medicines", [])

        if medicines:

            for medicine in medicines:

                st.write(
                    "Medicine:",
                    medicine.get("name", "Not available")
                )

                st.write(
                    "Dosage:",
                    medicine.get("dosage", "Not available")
                )

                st.write(
                    "Frequency:",
                    medicine.get("frequency", "Not available")
                )

                st.write(
                    "Duration:",
                    medicine.get("duration", "Not available")
                )

                st.divider()

        else:

            st.warning("No medicines found.")


        if st.button("💾 Save Prescription"):

            try:

                response = requests.post(
                    f"{API_URL}/save_prescription",
                    json=data
                )

                if response.status_code == 200:

                    st.success(
                        "Prescription saved successfully!"
                    )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))


        if st.button("📄 Generate PDF"):

            try:

                response = requests.post(
                    f"{API_URL}/pdf_report",
                    json=data
                )

                if response.status_code == 200:

                    result = response.json()

                    filename = result.get("file")

                    if filename:

                        try:

                            with open(
                                filename,
                                "rb"
                            ) as file:

                                st.download_button(
                                    "⬇️ Download PDF",
                                    file,
                                    file_name="prescription_report.pdf",
                                    mime="application/pdf"
                                )

                        except FileNotFoundError:

                            st.error(
                                "PDF was created on FastAPI server but could not be opened by Streamlit."
                            )

                    else:

                        st.error(
                            "PDF file was not created."
                        )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))


# =========================================================
# HISTORY
# =========================================================

with tab2:

    st.header("📚 Prescription History")

    if st.button("🔄 Load History"):

        try:

            response = requests.get(
                f"{API_URL}/get_prescriptions"
            )

            if response.status_code == 200:

                history = response.json()

                if history:

                    for item in history:

                        st.write(
                            "👤 Patient:",
                            item["patient_name"]
                        )

                        st.write(
                            "👨‍⚕️ Doctor:",
                            item["doctor_name"]
                        )

                        st.write(
                            "💊 Medicine:",
                            item["medicine_name"]
                        )

                        st.write(
                            "💉 Dosage:",
                            item["dosage"]
                        )

                        st.write(
                            "⏰ Frequency:",
                            item["frequency"]
                        )

                        st.write(
                            "📅 Duration:",
                            item["duration"]
                        )

                        st.divider()

                else:

                    st.info(
                        "No prescriptions found."
                    )

            else:

                st.error(response.text)

        except Exception as e:

            st.error(str(e))


# =========================================================
# LOCATION + PHARMACY
# =========================================================

with tab3:

    st.header("📍 Location")

    if st.button("Get Location"):

        try:

            response = requests.get(
                f"{API_URL}/get_location"
            )

            if response.status_code == 200:

                location = response.json()

                st.write(
                    "Latitude:",
                    location["latitude"]
                )

                st.write(
                    "Longitude:",
                    location["longitude"]
                )

            else:

                st.error(response.text)

        except Exception as e:

            st.error(str(e))


    st.header("🏥 Pharmacy Finder")

    if st.button("Find Pharmacies"):

        try:

            response = requests.get(
                f"{API_URL}/find_pharmacies"
            )

            if response.status_code == 200:

                pharmacies = response.json()

                for pharmacy in pharmacies:

                    st.write(
                        f"💊 {pharmacy['name']}"
                    )

                    url = (
                        "https://www.google.com/maps/search/"
                        f"?api=1&query="
                        f"{pharmacy['latitude']},"
                        f"{pharmacy['longitude']}"
                    )

                    st.markdown(
                        f"[📍 Open Google Maps]({url})"
                    )

                    st.divider()

            else:

                st.error(response.text)

        except Exception as e:

            st.error(str(e))


# =========================================================
# WARNINGS
# =========================================================

with tab4:

    st.header("⚠️ Critical Warnings")

    if st.button("Check Warnings"):

        if "prescription" not in st.session_state:

            st.warning(
                "Analyze prescription first."
            )

        else:

            medicines = st.session_state[
                "prescription"
            ].get(
                "medicines",
                []
            )

            try:

                response = requests.post(
                    f"{API_URL}/check_warnings",
                    json={
                        "medicines": medicines
                    }
                )

                if response.status_code == 200:

                    warnings = response.json()

                    if warnings:

                        for warning in warnings:

                            st.warning(warning)

                    else:

                        st.success(
                            "No critical warnings detected."
                        )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))


# =========================================================
# CHATBOT
# =========================================================

with tab5:

    st.header("🤖 MediGrid AI Chatbot")

    message = st.text_input(
        "Ask your question"
    )

    if st.button("💬 Ask AI"):

        if not message:

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    params={
                        "message": message
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.write(
                            result["response"]
                        )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))