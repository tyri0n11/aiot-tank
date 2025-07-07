import React from 'react'
import { Outlet } from 'react-router-dom'
import bgVideo from '@/assets/background.mp4'
const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <main className="w-full max-w-md p-6 bg-white rounded shadow-md">
        <video
                                autoPlay
                                loop
                                muted
                                playsInline
                                style={{
                                    position: 'absolute',
                                    width: '100%',
                                    height: '100%',
                                    objectFit: 'cover',
                                    top: 0,
                                    left: 0,
                                    zIndex: -1,
                                }}
                            >
                                <source src={bgVideo} type="video/mp4" />
                                Your browser does not support the video tag.
                            </video>
        <Outlet />
      </main>
      <footer className="mt-4 text-sm text-gray-500">
        © Main Layout
      </footer>
    </div>
  )
}

export default MainLayout
