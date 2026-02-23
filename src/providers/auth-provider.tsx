import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";

interface AuthContextValue {
  userName: string;
  isAuthenticated: boolean | null;
  checkAuthStatus: () => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [userName, setUserName] = useState("Yoonjae Park");
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  const checkAuthStatus = useCallback(async () => {
    try {
      const response = await fetch("/money/graphql", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query: "query { __typename }" }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.errors) {
          setIsAuthenticated(false);
        } else {
          setIsAuthenticated(true);
        }
      } else {
        setIsAuthenticated(false);
      }
    } catch {
      setIsAuthenticated(false);
    }
  }, []);

  const logout = useCallback(() => {
    setIsAuthenticated(false);
    setUserName("");
    fetch("/accounts/logout/", {
      method: "POST",
      credentials: "include",
    }).then(() => {
      window.location.assign("/login");
    });
  }, []);

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  return (
    <AuthContext.Provider value={{ userName, isAuthenticated, checkAuthStatus, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
