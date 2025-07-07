import { createContext, useContext, useState } from 'react'
import { login as apiLogin, register as apiRegister } from '../../api/auth'
import { useNavigate } from 'react-router'

type AuthContextType = {
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const navigate = useNavigate()
  const login = async (email: string, password: string) => {
    try {
      await apiLogin(email, password)
      setIsAuthenticated(true)
      navigate('/main')
    } catch (error) {
      setIsAuthenticated(false)
      throw error
    }
  }

  const register = async (name: string, email: string, password: string) => {
    try {
      await apiRegister(name, email, password)
      setIsAuthenticated(true)
    } catch (error) {
      setIsAuthenticated(false)
      throw error
    }
  }

  const logout = () => {
    setIsAuthenticated(false)
    // Xóa token nếu có
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)!