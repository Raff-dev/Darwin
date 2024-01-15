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
    conversation_id: number;
    conversation: Conversation;
}

export enum MessageType {
    SYSTEM = "system",
    USER = "user",
    AI = "ai",
}

async function getConversation(conversationId: number): Promise<Conversation> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}`);
    return response.json();
}

async function getMessages(conversationId: number): Promise<Message[]> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}/messages/`);
    return response.json();
}

async function createMessage(message: MessageCreate, conversationId: number): Promise<Message> {
    const response = await fetch(`${API_URLS.CONVERSATIONS}/${conversationId}/messages/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
    });
    return response.json();
}

export { createMessage, getConversation, getMessages };
