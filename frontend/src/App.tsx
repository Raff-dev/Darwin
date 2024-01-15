import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Chat from './Chat';
import Documents from './Documents';
import NewDocument from './NewDocument';

function App() {
  return (
    <BrowserRouter>
      <Container>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" href="/">Home</Button>
          <Typography sx={{ flexGrow: 1 }} />
          <Button color="inherit" href="/about">About</Button>
          <Button color="inherit" href="/documents">Documents</Button>
        </Toolbar>
      </AppBar>
        <Box sx={{ marginTop: '20px' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/documents" />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/documents/new" element={<NewDocument />} />
            <Route path="/documents/:document_id/chat" element={<Chat />} />
          </Routes>
        </Box>
      </Container>
    </BrowserRouter>
  );
}

export default App;
