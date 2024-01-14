import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Documents from './Documents';
import NewDocument from './NewDocument';

const documents = [
  { id: 1, name: 'Document 1' },
  { id: 2, name: 'Document 2' },
];

function App() {
  return (
    <BrowserRouter>
      <Container>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" href="/">Home</Button>
          <Typography sx={{ flexGrow: 1 }} />
          <Button color="inherit" href="/scores">Scores</Button>
          <Button color="inherit" href="/about">About</Button>
          <Button color="inherit" href="/documents">Documents</Button>
        </Toolbar>
      </AppBar>
        <Box sx={{ marginTop: '20px' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/documents" />} />
            <Route path="/documents" element={<Documents documents={documents} />} />
            <Route path="/documents/new" element={<NewDocument />} />
          </Routes>
        </Box>
      </Container>
    </BrowserRouter>
  );
}

export default App;
