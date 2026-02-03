import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import NmapScanner from './pages/NmapScanner';
import SubfinderScanner from './pages/SubfinderScanner';
import BruteForce from './pages/BruteForce';
import XSSScanner from './pages/XSSScanner';

function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', width: '100%' }}>
        <Sidebar />
        <main style={{ flex: 1, padding: '32px', overflowY: 'auto' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/nmap" element={<NmapScanner />} />
            <Route path="/subfinder" element={<SubfinderScanner />} />
            <Route path="/bruteforce" element={<BruteForce />} />
            <Route path="/xss" element={<XSSScanner />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
