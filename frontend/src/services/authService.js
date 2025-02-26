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
  try {
    const firebaseResult = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    const firebaseUser = firebaseResult.user;

    // Hacer la petición al backend
    const backendResponse = await backendAPI.post("auth/login", {
      username: email,
      email: email,
      password: password,
    });

    // Asegurarnos de que devolvemos el objeto en el formato correcto
    return {
      user: {
        username: backendResponse.data.username,
        email: firebaseUser.email,
      },
      access_token: backendResponse.data.access_token,
    };
  } catch (error) {
    console.error("Error en login:", error);
    throw error;
  }
};

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;

    const payload = {
      username: user.email, // Usar email como username
      email: user.email,
      password: user.uid,
    };

    let backendResponse;
    try {
      // Intentar login primero
      backendResponse = await backendAPI.post("auth/login", payload);
    } catch (e) {
      if (e.response?.status === 401) {
        // Si falla el login, intentar registro
        await backendAPI.post("auth/register", payload);
        // Y luego login
        backendResponse = await backendAPI.post("auth/login", payload);
      } else {
        throw e;
      }
    }

    return {
      user: {
        username: backendResponse.data.username,
        email: user.email,
      },
      access_token: backendResponse.data.access_token,
    };
  } catch (error) {
    console.error("Error during Google sign-in:", error);
    throw error;
  }
};
