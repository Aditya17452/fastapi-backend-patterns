from services.llm_service import get_response


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bye....")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = get_response(messages)

    print("AI:", response)

    messages.append({
        "role": "assistant",
        "content": response
    })