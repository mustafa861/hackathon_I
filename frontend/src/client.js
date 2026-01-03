import { AuthProvider } from './context/AuthContext';

// This is the client entry point that wraps the entire app
const wrapRootElement = ({ element }) => {
  return (
    <AuthProvider>
      {element}
    </AuthProvider>
  );
};

export { wrapRootElement };