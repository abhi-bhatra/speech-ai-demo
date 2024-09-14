import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

# Function 1: Speech-to-Text
def recognize_from_microphone():
    # Speech recognition configuration
    speech_config = speechsdk.SpeechConfig(subscription='25eaf0696e92414c861deb4b362c2719', region='eastus')
    speech_config.speech_recognition_language = "en-US"
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = speech_recognition_result.text
        print("Recognized: {}".format(recognized_text))
        return recognized_text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return None

# Function 2: GPT-3.5 Response from OpenAI
def gpt_response(prompt_text):
    client = AzureOpenAI(
        api_key="a93bcfa38a6c48a0985a605093c17f49",
        api_version="2024-02-01",
        azure_endpoint="https://demo-ai-summit-openai.openai.azure.com/"
    )
    deployment_name = 'openai-deployment'  # gpt-35-turbo-instruct
    
    print(f"Sending your prompt to GPT-3: {prompt_text}")
    response = client.completions.create(model=deployment_name, prompt=prompt_text, max_tokens=100)
    
    # Extract only the text from the response
    gpt_reply = response.choices[0].text.strip()
    
    print(f"GPT-3 Response: {gpt_reply}\n\n")
    return gpt_reply

def synthesize_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription='25eaf0696e92414c861deb4b362c2719', region='eastus')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

# Main Loop: Combining Speech-to-Text and GPT Response
def main_loop():
    print("Welcome! Press Enter to speak to GPT, or press any other key to quit.")
    
    while True:
        # Prompt user to continue or stop
        user_input = input("Press Enter to speak or any other key to quit: ")
        
        if user_input == "":
            # Capture speech input
            spoken_text = recognize_from_microphone()
            
            if spoken_text:
                # Pass the recognized text to GPT-3
                gpt_reply = gpt_response(spoken_text)
                synthesize_speech(gpt_reply)
        else:
            print("Exiting the interaction.")
            break

# Start the interaction loop
if __name__ == "__main__":
    main_loop()
