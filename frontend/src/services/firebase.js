import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCIPH9gri4dqlFRzc3N-mUvk6kV4H1B7oU",
  authDomain: "expenses-traker-f3fcc.firebaseapp.com",
  projectId: "expenses-traker-f3fcc",
  storageBucket: "expenses-traker-f3fcc.firebasestorage.app",
  messagingSenderId: "396367934349",
  appId: "1:396367934349:web:517f583db5ef48606d43c4",
  measurementId: "G-CB1CBDK624",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export {
  auth,
  googleProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
};
