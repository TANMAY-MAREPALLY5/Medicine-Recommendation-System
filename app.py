import streamlit as st
from med_recomm import recommend_medicine1,get_composition,get_side_effects,get_manufacturer,get_image_url

# Set page title and favicon
st.set_page_config(page_title="Medicine Recommendation System", page_icon=":pill:")

def display_symptoms(medical_history):
    symptoms = {
        "ANXIETY": ["Feeling nervous, restless or tense",
                    "Having a sense of impending danger, panic or doom",
                    "Having an increased heart rate",
                    "Breathing rapidly (hyperventilation)",
                    "Sweating",
                    "Having trouble sleeping"],
        "ARTHRITIS": ["Pain",
                      "Stiffness",
                      "Swelling",
                      "Redness",
                      "Decreased range of motion"],
        "ASTHMA": ["Shortness of breath",
                   "Chest tightness or pain",
                   "Wheezing when exhaling",
                   "Trouble sleeping",
                   "Coughing"],
        "BLOOD CLOTS": ["Arms and legs: Pain or tenderness, swelling, or warm feeling",
                        "Brain: Trouble speaking; vision changes; sudden, strong headache; dizziness; or weakness in face, arms, or legs",
                        "Heart: Pain in the chest or other part of the upper body, breathing difficulties, sweating, nausea, or light-headedness",
                        "Lungs: Chest pain, difficulty breathing, rapid heartbeat, sweating, fever, or coughing up blood"],
        "CHRONIC PAIN": ["Arthritis, or joint pain.",
                         "Back pain.",
                         "Neck pain.",
                         "Cancer pain near a tumor.",
                         "Headaches, including migraines"],
        "DEPRESSION": ["Feelings of sadness, tearfulness, emptiness or hopelessness",
                       "Angry outbursts, irritability or frustration, even over small matters",
                       "Loss of interest or pleasure in most or all normal activities, such as sex, hobbies or sports",
                       "Sleep disturbances, including insomnia or sleeping too much."],
        "DIABETES": ["Feeling more thirsty than usual.",
                     "Urinating often.",
                     "Losing weight without trying.",
                     "Feeling irritable or having other mood changes.",
                     "Having blurry vision.",
                     "Having slow-healing sores."],
        "HIGH BLOOD PRESSURE": ["severe headaches.",
                                 "chest pain.",
                                 "dizziness.",
                                 "difficulty breathing.",
                                 "nausea.",
                                 "vomiting."],
        "HIV": ["Fever.",
                "Fatigue.",
                "Swollen lymph glands, which are often one of the first symptoms of HIV infection.",
                "Diarrhea.",
                "Weight loss.",
                "Oral yeast infection, also called thrush.",
                "Pneumonia."],
        "SEIZURES": ["Temporary confusion.",
                     "A staring spell.",
                     "Jerking movements of the arms and legs that can't be controlled.",
                     "Loss of consciousness or awareness.",
                     "Cognitive or emotional changes"]
    }

    if medical_history in symptoms:
        st.write(f"SYMPTOMS FOR {medical_history}:")
        for symptom in symptoms[medical_history]:
            st.write(symptom)
        st.write("")  
    else:
        st.write("No symptoms available for the selected medical history.")

def display_medical_history():
    st.write("")
    st.write("")
    st.write("")
    st.write("Select from the following medical histories:")
    medical_histories = st.multiselect("Choose medical histories", ["ANXIETY", "ARTHRITIS", "ASTHMA", "BLOOD CLOTS", "CHRONIC PAIN", "DEPRESSION", "DIABETES", "HIGH BLOOD PRESSURE", "HIV", "SEIZURES"])
    if medical_histories:
        for history in medical_histories:
            display_symptoms(history)
    else:
        st.write("No medical history selected.")

def get_recommendations():  
    st.write("")
    st.write("")
    st.write("")
    disease = st.text_input("Based on Condition/Symptom: ")
    if disease:
        recommendations = recommend_medicine1([disease])
        if recommendations != "No medicines found for this disease.":
            st.write(f"Top 5 recommended medicines for {disease} are:")
            for med in recommendations[:5]:
                medicine = med[0]  
                st.write(f"Medicine: {medicine}")
                
                composition = get_composition(medicine)
                side_effects = get_side_effects(medicine)
                manufacturer = get_manufacturer(medicine)
                image_url = get_image_url(medicine)
                st.write(f"Composition: {composition}")
                st.write(f"Side Effects: {side_effects}")
                st.write(f"Manufacturer: {manufacturer}")
                st.image(image_url)
                st.write("")  
        else:
            st.write(f"No medicines found for {disease}")

def main():
    st.title("Medicine Recommendation System")
    option = st.sidebar.selectbox("Choose an option:", ["Select Medical Histories", "Enter Condition/Symptom"])

    if option == "Select Medical Histories":
        display_medical_history()
    elif option == "Enter Condition/Symptom":
        get_recommendations()

if __name__ == "__main__":
    main()
