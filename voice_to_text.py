import gradio as gr
import speech_recognition as sr

def transcribe_audio(audio_filepath):
    if audio_filepath is None:
        return "No audio recorded. Please record something first."
    
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_filepath) as source:
            # Adjust for noise just in case, though usually handled by the recording environment
            # r.adjust_for_ambient_noise(source) 
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio. Please try speaking more clearly."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"An error occurred: {e}"

# Create a premium-feeling UI using Blocks and a soft theme
with gr.Blocks(theme=gr.themes.Soft(), title="Voice to Text Pro") as app:
    gr.Markdown(
        """
        # 🎙️ Voice to Text Pro
        ### Convert your speech into text instantly.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath", 
                label="Record Input"
            )
            
            with gr.Row():
                clear_btn = gr.ClearButton(components=[audio_input], value="Clear Recording")
                transcribe_btn = gr.Button("Transcribe Audio", variant="primary")
        
        with gr.Column(scale=1):
            text_output = gr.Textbox(
                label="Transcription Output", 
                placeholder="Transcription will appear here...",
                lines=10
            )
            
    # Connect the button to the function
    transcribe_btn.click(
        fn=transcribe_audio, 
        inputs=audio_input, 
        outputs=text_output
    )

if __name__ == "__main__":
    app.launch()
