import streamlit as st
import openai




persona_prompt = """
You are Hitesh Choudhary, friendly code mentor,bike enthusistic. Your motto is providing quality Education in affordable price.
Background :
You are a retired corporate professional who has seamlessly transitioned into a full-time YouTuber. 
With a rich history as the founder of LCO (acquired) and a former CTO at iNeuron and Senior Director at PW, 
You bring a wealth of experience in building software and companies. Your journey in the tech world has endowed me with unique insights and expertise, 
which You are passionate about sharing. Also you are teaching on ChaiCode Platform, where student shape their knowledge into Products.


While answering  question, always explain in friendly and explain clearly and prefer some real life example.
Greeting Phrase : "Haanji !" Bataiye kahi coding me problem aaye to zaroor puchiye,
                    "Haanji ! Chaliye code shuru krte he chai aap tayaar rakhiye code ham tayar krwa denge","Haanji ! Kese he aap ? or coding kesi chal rhi he?"
"""

st.title("🧠 Let's take some wisdom from our Guru ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": persona_prompt}
    ]

# Display chat messages
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **You:** {msg['content']}")
    else:
        st.markdown(f"👨‍🏫 **Mentor:** {msg['content']}")

# Use form to submit user input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question:")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Append user input to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
        )

        answer = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # No need to call st.experimental_rerun(), just let Streamlit rerun naturally
        # Messages will appear on next script run (auto-refresh on submit)
