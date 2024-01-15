import { Box, Button, Container, Typography } from "@mui/material";
import React, { ChangeEvent, useState } from "react";
import { createDocument } from "./api/documents";

const NewDocument: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<boolean>(false); // Add success state

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files && event.target.files[0];
        if (selectedFile) {
            if (selectedFile.type !== "application/pdf") {
                setError("Please choose a PDF file");
            } else {
                setError(null);
                setFile(selectedFile);
            }
        }
    };

    const handleSubmit = async () => {
        if (!file) {
            setError("No file chosen");
            return;
        }

        try {
            await createDocument(file);
            setSuccess(true);
            setError(null);
        } catch (error) {
            setSuccess(false);
            setError("Failed to upload file");
        }
    };

    return (
        <Container maxWidth="sm">
            <Typography variant="h3" align="center" gutterBottom>
                Upload a Document
            </Typography>
            <Box
                component="form"
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "stretch",
                    width: "100%",
                }}
                noValidate
                autoComplete="off"
            >
                <label htmlFor="file-upload" style={{ display: "flex", alignItems: "center" }}>
                    <Button variant="outlined" component="span">
                        Choose File
                    </Button>
                    <input id="file-upload" type="file" hidden accept="application/pdf" onChange={handleFileChange} />
                    <Typography style={{ marginLeft: "8px" }}>{file ? file.name : "No file chosen"}</Typography>
                </label>
                {error && (
                    <Typography sx={{ color: "red" }}>{error}</Typography>
                )}
                {success && ( // Render success message if success state is true
                    <Typography sx={{ color: "green" }}>File uploaded successfully</Typography>
                )}
                <Button variant="contained" size="large" onClick={handleSubmit}>
                    Submit
                </Button>
            </Box>
        </Container>
    );
};

export default NewDocument;
