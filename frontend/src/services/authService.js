import axios from "axios";
import {
  auth,
  googleProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "./firebase";

const backendAPI = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Registro con email. Se usa la contraseña para Firebase y también se envía al backend.
export const registerWithEmail = async (email, password, displayName) => {
  const result = await createUserWithEmailAndPassword(auth, email, password);
  const user = result.user;
  const payload = { username: displayName, email: user.email, password }; // En backend se debe procesar esta info
  await backendAPI.post("auth/register", payload);
  return user;
};

// Login con email.
export const loginWithEmail = async (email, password) => {
  const result = await signInWithEmailAndPassword(auth, email, password);
  const user = result.user;
  // Opcional: enviar al backend si se requiere crear sesión

  return user;
};

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    console.log("Google sign-in response:", result);

    const user = result.user;
    const payload = {
      username: user.displayName,
      email: user.email,
      password: user.uid,
    };

    console.log("Payload for backend:", payload);

    let backendResponse;
    try {
      backendResponse = await backendAPI.post("auth/register", payload);
    } catch (e) {
      if (e.response && e.response.status === 400) {
        // El usuario ya está autenticado, se hace POST a login
        backendResponse = await backendAPI.post("auth/login", payload);
      } else {
        throw e;
      }
    }

    console.log("Backend response:", backendResponse.data);
    return user;
  } catch (error) {
    console.error("Error during Google sign-in:", error);
    throw error;
  }
};
