import API_URLS from '../api/config';

export interface Conversation {
    id: number;
    messages: Message[];
}

export interface ConversationCreate {
}


export interface MessageCreate {
    text: string;
    type: MessageType;
}

export interface Message {
    id: number;
    text: string;
    type: MessageType;
}


export enum MessageType {
    SYSTEM = "system",
    USER = "human",
    AI = "ai",
    FUNCTION = "function",
}

async function getConversation(conversationId: number): Promise<Conversation> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}`);
    return response.json();
}

async function getMessages(conversationId: number): Promise<Message[]> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}/messages/`);
    return await response.json();
}

async function createMessage(
    userMessage: MessageCreate,
    conversationId: number,
    setAiStreamMessage: (text: string) => void,
): Promise<void> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}/messages/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userMessage),
    });

    if (!response.body) {
        throw new Error("No response body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let text = "";

    while (true) {
        const { done, value } = await reader.read();

        if (done) {
            break;
        }

        text += decoder.decode(value);
        setAiStreamMessage(text);
    }
}

export { createMessage, getConversation, getMessages };
