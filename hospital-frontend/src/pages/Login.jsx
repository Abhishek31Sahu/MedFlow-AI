import { useState } from "react";
import {
  Box,
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import {
  Visibility,
  VisibilityOff,
  LocalHospital,
  Lock,
  Person,
} from "@mui/icons-material";

import { login } from "../services/authService";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      await login({
        username,
        password,
      });

      window.location.href = "/dashboard";
    } catch (err) {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-100 to-blue-50 p-6">
      <Paper
        elevation={12}
        className="w-full max-w-6xl rounded-3xl overflow-hidden grid md:grid-cols-2"
      >
        {/* LEFT */}

        <Box className="bg-blue-600 text-white p-12 flex flex-col justify-center">
          <Box className="flex items-center gap-3 mb-8">
            <LocalHospital sx={{ fontSize: 50 }} />

            <Typography variant="h4" fontWeight="bold">
              AI Hospital Workflow
            </Typography>
          </Box>

          <Typography variant="h3" fontWeight="bold" mb={2}>
            Smarter Care.
            <br />
            Better Workflow.
          </Typography>

          <Typography fontSize={18}>
            Intelligent hospital management powered by AI, helping doctors,
            nurses and administrators manage patient workflows efficiently.
          </Typography>

          <Box mt={8}>
            <Typography mb={2}>✔ Secure JWT Authentication</Typography>

            <Typography mb={2}>✔ Role Based Access</Typography>

            <Typography mb={2}>✔ AI Assisted Hospital Workflow</Typography>

            <Typography>✔ FHIR Integrated Platform</Typography>
          </Box>
        </Box>

        {/* RIGHT */}

        <Box
          component="form"
          onSubmit={handleLogin}
          className="p-12 flex flex-col justify-center"
        >
          <Typography variant="h4" fontWeight="bold" textAlign="center" mb={1}>
            Welcome Back
          </Typography>

          <Typography color="text.secondary" textAlign="center" mb={5}>
            Sign in to continue
          </Typography>

          <TextField
            fullWidth
            label="Username"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Person />
                </InputAdornment>
              ),
            }}
          />

          <TextField
            fullWidth
            type={showPassword ? "text" : "password"}
            label="Password"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock />
                </InputAdornment>
              ),

              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => setShowPassword(!showPassword)}>
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Box className="flex justify-between items-center mt-3">
            <FormControlLabel control={<Checkbox />} label="Remember Me" />

            <Button>Forgot Password?</Button>
          </Box>

          {error && (
            <Typography color="error" mt={2}>
              {error}
            </Typography>
          )}

          <Button
            fullWidth
            variant="contained"
            size="large"
            sx={{
              mt: 4,
              py: 1.5,
              borderRadius: 3,
            }}
            disabled={loading}
            type="submit"
          >
            {loading ? (
              <CircularProgress size={25} color="inherit" />
            ) : (
              "Sign In"
            )}
          </Button>

          <Typography mt={5} textAlign="center" color="text.secondary">
            Need an account?
            <br />
            Contact Hospital Administrator
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}
