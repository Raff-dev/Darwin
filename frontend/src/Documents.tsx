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
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { deleteDocument, getDocuments } from "./api/services";

interface Document {
    id: number;
    filename: string;
}

const Documents: React.FC = () => {
    const [documents, setDocuments] = useState<Document[]>([]);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const data = await getDocuments();
            setDocuments(data);
        } catch (error) {
            console.error("Error fetching documents:", error);
        }
    };

    const handleDelete = async (id: number) => {
        try {
            deleteDocument(id);
            setDocuments(documents.filter((document) => document.id !== id));
        } catch (error) {
            console.error("Error deleting document:", error);
        }
    };

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
                            <TableCell>{document.filename}</TableCell>
                            <TableCell sx={{ textAlign: "right" }}>
                                <Button variant="contained" color="primary" sx={{ marginRight: 1 }}>
                                    Chat
                                </Button>
                                <Button variant="contained" color="secondary" onClick={() => handleDelete(document.id)}>
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
