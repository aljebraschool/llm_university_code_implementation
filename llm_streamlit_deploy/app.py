import streamlit as st
import cohere
import json
import os
import textwrap

#set up cohere client
co = cohere.ClientV2("VKxoCS7wrKZgmI7GMtm0OTpDYNNoFGDw3mKEdQQT")

#creating a prompt that contains some examples of industry with respective startup idea

def generate_idea(industry, temperature):
    prompt = f"""
            Generate a startup idea given the industry, and return the startup idea without any commentary.
            
            Industry : workspace
            Startup Idea : A placeform that generates slide deck content automatically based on a given outline
            
            Industry : Home decor
            Startup Idea : An app that calculates the best position of your indoor plant for your aparment
            
            Industry: Healthcare
            Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
            
            Industry: Education
            Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
            
            Industry : {industry}
            Startup Idea : 

        """
    response = co.chat(model = "command-r-plus-08-2024", messages = [{"role": "user", "content": prompt}], temperature = temperature)

    return response.message.content[0].text


def generate_name(idea, temperature ):
    prompt = f"""
        Generate a startup name given the startup idea. Return the startup name and without additional commentary.
        
        Startup Idea: A platform that generates slide deck contents automatically based on a given outline
        Startup Name: Deckerize
        
        Startup Idea: An app that calculates the best position of your indoor plants for your apartment
        Startup Name: Planteasy 
        
        Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
        Startup Name: Hearspan
        
        Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
        Startup Name: Prime Age
        
        Startup Idea: {idea} 
        Startup Name:

        """

    # Call the Cohere Chat endpoint
    response = co.chat(
        messages=[{"role": "user", "content": prompt}],
        model="command-r-plus-08-2024",
        temperature=temperature)

    return response.message.content[0].text


"""Setup Streamlit for frontend Application"""

st.title("🚀 Startup Idea Generator")
form = st.form(key= "user settings")

with form:
    # User input - Industry name
    industry_input = st.text_input("Industry", key = "industry_input")

    # Create a two-column view
    column_1, column_2 = st.columns(2)

    with column_1:
        # User input - The number of ideas to generate
        num_input = st.slider("Number of ideas", value = 3, min_value = 1, max_value = 10)

    with column_2:
        creativity_input = st.slider("Creativity", value = 0.5, min_value = 0.1, max_value = 0.9)

    # Submit button to start generating ideas
    generate_button = form.form_submit_button("Generate Idea")

    if generate_button:
        if industry_input == "":
            st.error("Industry field cannot be blank")
        else:
            my_bar = st.progress(0.5)
            st.subheader("Startup Ideas")

            for i in range(num_input):
                st.markdown("""---""")
                startup_idea = generate_idea(industry_input, creativity_input )
                startup_name = generate_name(startup_idea, creativity_input)
                st.markdown("#### " + startup_name + "\n")
                st.write(startup_idea)
                my_bar.progress((i + 1) / num_input)


# if __name__ == "__main__":
#     industry = "Education"
#
#     generated_idea = generate_idea(industry, temperature = 0.5)
#
#     print(f"Startup idea generated {generated_idea}")
#
#     idea = "A platform that can help math enthusiast learn together"
#
#     generated_name = generate_name(idea, 0.5)
#
#     print(f"Generated name for {idea} is {generated_name}")


