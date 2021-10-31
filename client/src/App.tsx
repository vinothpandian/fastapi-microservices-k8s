import {
  Box,
  Button,
  ChakraProvider,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  ListItem,
  SimpleGrid,
  UnorderedList,
} from "@chakra-ui/react";
import axios from "axios";
import React, { ReactElement } from "react";
import { Posts } from "./types";

interface HeaderComponentProps {
  title: string;
  setTitle: React.Dispatch<React.SetStateAction<string>>;
}

function HeaderComponent({
  title,
  setTitle,
}: HeaderComponentProps): ReactElement {
  return (
    <Box p="8">
      <Heading sx={{ pb: 2 }} size="xl">
        Create a post!
      </Heading>
      <form>
        <FormControl sx={{ p: 2 }} id="post-title" isRequired>
          <FormLabel>Post title</FormLabel>
          <Input
            required
            placeholder="e.g. Hello!"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </FormControl>
        <Button
          sx={{ mt: 2 }}
          type="submit"
          colorScheme="green"
          onClick={() => {
            axios.post("http://localhost:4000/posts/create/", {
              title,
            });
          }}
        >
          Submit post
        </Button>
      </form>
    </Box>
  );
}

interface PostsComponentProps {
  posts: Posts;
  commentText: string;
  setCommentText: React.Dispatch<React.SetStateAction<string>>;
}

function PostsComponent({
  posts,
  commentText,
  setCommentText,
}: PostsComponentProps): ReactElement {
  return (
    <Box p="8">
      <Heading size="xl">Posts</Heading>
      <SimpleGrid w="100%" p="2" columns={3} spacing={8}>
        {Object.entries(posts).map(([postId, post]) => (
          <Box key={postId} border="1px solid #ccc" borderRadius={2} p="4">
            <Heading>{post.title}</Heading>
            <UnorderedList>
              {post.comments.map((comment) => (
                <ListItem key={comment.id}>{comment.comment}</ListItem>
              ))}
            </UnorderedList>
            <form>
              <FormControl id="comment-text" isRequired>
                <FormLabel>Comment here</FormLabel>
                <Input
                  placeholder="e.g. This sux!"
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                />
              </FormControl>
              <Button
                type="submit"
                onClick={() => {
                  axios.post("http://localhost:4001/comments/create/", {
                    post_id: postId,
                    comment: commentText,
                  });
                }}
              >
                Add comment
              </Button>
            </form>
          </Box>
        ))}
      </SimpleGrid>
    </Box>
  );
}

function App(): ReactElement {
  const [posts, setPosts] = React.useState<Posts>({});
  const [title, setTitle] = React.useState<string>("");
  const [commentText, setCommentText] = React.useState<string>("");

  const updatePosts = async () => {
    const response = await axios.get<Posts>("http://localhost:4002/posts");
    if (response.status !== 200) {
      return;
    }
    setPosts(response.data);
  };

  React.useEffect(() => {
    updatePosts();
  }, []);

  return (
    <ChakraProvider>
      <Container maxW="container.lg" m="8">
        <HeaderComponent title={title} setTitle={setTitle} />
        <PostsComponent
          posts={posts}
          commentText={commentText}
          setCommentText={setCommentText}
        />
      </Container>
    </ChakraProvider>
  );
}

export default App;
