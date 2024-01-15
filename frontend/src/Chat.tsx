import { Box, Button, Container, MenuItem, Select, SelectChangeEvent, TextField } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { Conversation, Message, MessageType, createMessage, getConversations, getMessages } from './api/conversations';

function Chat() {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        async function fetchConversations() {
            const conversations = await getConversations();
            setConversations(conversations);
            if (conversations.length > 0) {
                setSelectedConversation(conversations[0]);
            }
        }
        fetchConversations();
    }, []);

    useEffect(() => {
        async function fetchMessages() {
            if (selectedConversation) {
                const messages = await getMessages(selectedConversation.id);
                setMessages(messages);
            }
        }
        fetchMessages();
    }, [selectedConversation]);

    const handleConversationChange = (event: SelectChangeEvent<number>) => {
        const selectedId = Number(event.target.value);
        const selected = conversations.find(c => c.id === selectedId) || null;
        setSelectedConversation(selected);
    };

    const handleNewMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setNewMessage(event.target.value);
    };


    const handleNewMessageSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (selectedConversation && newMessage.trim() !== '') {
            const message = await createMessage({ text: newMessage, type: MessageType.User }, selectedConversation.id);
            setMessages([...messages, message]);
            setNewMessage('');
        }
    };

    return (
        <Container>
            <Select value={selectedConversation?.id || ''} onChange={handleConversationChange}>
                {conversations.map(c => <MenuItem key={c.id} value={c.id}>Conversation {c.id}</MenuItem>)}
            </Select>
            <Box sx={{ my: 2 }}>
                {messages.map((m, i) => <p key={i}>{m.text}</p>)}
            </Box>
            <form onSubmit={handleNewMessageSubmit}>
                <TextField fullWidth value={newMessage} onChange={handleNewMessageChange} />
                <Button type="submit">Send</Button>
            </form>
        </Container>
    );
}

export default Chat;
