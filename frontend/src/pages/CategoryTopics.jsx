import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api";
import {
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Stack,
  Box,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";
import ArrowBack from "@mui/icons-material/ArrowBack";

const CategoryTopics = () => {
  const { categoryId } = useParams();
  const [topics, setTopics] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTopics = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/topics/category/${categoryId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTopics(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchTopics();
  }, [categoryId]);

  const viewTopic = (topicId) => {
    navigate(`/topics/${topicId}/replies`);
  };

  const lockTopic = async (topicId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.put(
        `/topics/${topicId}/lock`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setTopics((prevTopics) =>
        prevTopics.map((topic) =>
          topic.id === topicId ? { ...topic, locked: true } : topic
        )
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ padding: "20px" }}>
        <Typography component="h1" variant="h5">
          Topics in Category {categoryId}
        </Typography>
        {topics.map((topic) => (
          <Card key={topic.id} sx={{ margin: "20px 0" }}>
            <CardContent>
              <Typography variant="h6">{topic.title}</Typography>
              <Stack direction="row" spacing={2}>
                <Button variant="outlined" onClick={() => viewTopic(topic.id)}>
                  View Topic
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => lockTopic(topic.id)}
                  disabled={topic.locked}
                >
                  {topic.locked ? "Locked" : "Lock Topic"}
                </Button>
              </Stack>
            </CardContent>
          </Card>
        ))}
        <Box sx={{ textAlign: "right", marginTop: 2 }}>
          <Link to="/categories" style={{ textDecoration: "none" }}>
            <ArrowBack sx={{ marginRight: 1 }} />
            Back to Categories
          </Link>
        </Box>
      </Container>
      <Footer />
    </>
  );
};

export default CategoryTopics;
