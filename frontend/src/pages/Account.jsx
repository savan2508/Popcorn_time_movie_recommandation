import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Container, Typography, Box } from "@mui/material";

const Account = () => {
  const { userInfo } = useContext(AuthContext);

  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4">Account Information</Typography>
        {userInfo ? (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6">Username: {userInfo.username}</Typography>
            <Typography variant="h6">
              Name: {userInfo.first_name} {userInfo.last_name}
            </Typography>
            <Typography variant="h6">Email: {userInfo.email}</Typography>
            <Typography variant="h6">Age: {userInfo.age}</Typography>
            <Typography variant="h6">Gender: {userInfo.gender}</Typography>
            <Typography variant="h6">
              Occupation: {userInfo.occupation}
            </Typography>
            <Typography variant="h6">
              Preferred Genre: {userInfo.preferred_genre}
            </Typography>
            <Typography variant="h6">
              Recommended Genre: {userInfo.recommended_genre}
            </Typography>
          </Box>
        ) : (
          <Typography variant="h6">Loading...</Typography>
        )}
      </Box>
    </Container>
  );
};

export default Account;
