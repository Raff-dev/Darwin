import { Button, Grid, MenuItem, Select, SelectChangeEvent, TextField, Typography } from '@mui/material';
import React, { useEffect, useRef, useState } from 'react';
import { Conversation, Message, MessageType, createMessage, getMessages } from './api/conversations';
import { Document, createConversation, getConversations, getDocument } from './api/documents';

import { useParams } from 'react-router-dom';


function Chat() {
    const { document_id } = useParams<{ document_id: string }>();
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [document, setDocument] = useState<Document | null>(null);
    const messagesContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        async function fetchDocument() {
            const document = await getDocument(Number(document_id));
            setDocument(document);
        }
        fetchDocument();
    }, [document_id]);

    useEffect(() => {
        async function fetchConversations() {
            if (!document) {
                return;
            }
            const conversations = await getConversations(document);
            setConversations(conversations);
            if (conversations.length > 0) {
                setSelectedConversation(conversations[0]);
            } else {
                handleCreateConversation();
            }
        }
        fetchConversations();
    }, [document]);

    useEffect(() => {
        async function fetchMessages() {
            if (selectedConversation && selectedConversation.id) {
                const messages = await getMessages(selectedConversation.id);
                setMessages(messages);
            }
        }
        fetchMessages();
    }, [selectedConversation]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

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
        if (selectedConversation && selectedConversation.id && newMessage.trim() !== '') {
            const message = await createMessage({ text: newMessage, type: MessageType.USER }, selectedConversation.id);
            setMessages([...messages, message]);
            setNewMessage('');
        }
    };

    const handleCreateConversation = async () => {
        if (!document) {
            return;
        }

        const newConversation = await createConversation(document, {});
        setSelectedConversation(newConversation);
        setConversations([...conversations, newConversation]);
    };

    const scrollToBottom = () => {
        if (messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
    };

    return (
        <Grid container direction="column">
            <Grid item xs>
                <Grid container alignItems="center" spacing={1}>
                    <Grid item>
                        <Select sx={{ minWidth: 200 }} value={selectedConversation?.id || ''} onChange={handleConversationChange}>
                            {conversations.map(c => <MenuItem key={c.id} value={c.id}>Conversation {c.id}</MenuItem>)}
                        </Select>
                    </Grid>
                    <Grid item >
                        {document && <Typography sx={{ fontWeight: 'bold', fontVariant:"small-caps" }}>{document.filename}</Typography>}
                    </Grid>
                    <Grid item sx={{ flexGrow: 1 }} />
                    <Grid item>
                        <Button variant="outlined" onClick={handleCreateConversation}>New</Button>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item xs="auto" sx={{ outline: '1px solid #3333', height: "70vh", overflow: 'auto', padding: '20px 20px', margin: '10px 0' }} ref={messagesContainerRef}>
                <Grid container spacing={1} direction="column">
                    {messages && messages.map((m, i) => (
                        <Grid container direction="column" key={i} sx={{padding: "5px"}}>
                            <Typography  sx={{ fontWeight: 'bold', fontVariant:"small-caps" }}>{m.type}</Typography>
                            <Typography>{m.text}</Typography>
                        </Grid>
                    ))}
                </Grid>
            </Grid>
            <Grid item xs>
                <form onSubmit={handleNewMessageSubmit} >
                    <Grid container alignItems="center" mt={2}>
                        <Grid item sx={{ flexGrow: 1 }}>
                            <TextField fullWidth value={newMessage} onChange={handleNewMessageChange}  />
                        </Grid>
                        <Grid item>
                            <Button type="submit">Send</Button>
                        </Grid>
                    </Grid>
                </form>
            </Grid>
        </Grid>
    );
}

export default Chat;
