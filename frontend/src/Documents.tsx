import {
    Button,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";

interface Document {
    id: number;
    name: string;
}

interface DocumentsProps {
    documents: Document[];
}

const Documents: React.FC<DocumentsProps> = ({ documents }) => {
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={3}>
                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                <Typography variant="h4">Your Documents</Typography>
                                <Button variant="contained" color="primary" component={Link} to="/documents/new">
                                    New
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell sx={{ textAlign: "right" }}>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {documents.map((document) => (
                        <TableRow key={document.id}>
                            <TableCell>{document.id}</TableCell>
                            <TableCell>{document.name}</TableCell>
                            <TableCell sx={{ textAlign: "right" }}>
                                <Button variant="contained" color="primary" sx={{ marginRight: 1 }}>
                                    Chat
                                </Button>
                                <Button variant="contained" color="secondary">
                                    Delete
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default Documents;
