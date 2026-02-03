import { useState } from 'react';
import axios from 'axios';
import ScannerLayout from '../components/ScannerLayout';
import ResultsDisplay from '../components/ResultsDisplay';
import { Play } from 'lucide-react';

const NmapScanner = () => {
    const [target, setTarget] = useState('');
    const [ports, setPorts] = useState('common');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleScan = async (e) => {
        e.preventDefault();
        if (!target) return;

        setLoading(true);
        setResults(null);
        setError(null);

        try {
            // Use config or env for base URL in prod
            const response = await axios.post('http://localhost:8000/api/scan/nmap', {
                target,
                ports
            });
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScannerLayout
            title="Nmap Port Scanner"
            description="Perform network reconnaissance to identify open ports, services, and potential vulnerabilities on target systems."
            badge="Network"
        >
            <div className="card" style={{ maxWidth: '800px' }}>
                <form onSubmit={handleScan} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Target (IP or Domain)</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g., 192.168.1.1 or example.com"
                            value={target}
                            onChange={(e) => setTarget(e.target.value)}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Scan Type</label>
                        <select
                            className="input"
                            value={ports}
                            onChange={(e) => setPorts(e.target.value)}
                        >
                            <option value="common">Common Ports (Top 1000)</option>
                            <option value="all">All Ports (1-65535)</option>
                            <option value="80,443,8080,22,21">Web & Infrastructure (80, 443, 8080, 22, 21)</option>
                        </select>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ alignSelf: 'flex-start' }}
                        disabled={loading}
                    >
                        {loading ? 'Scanning...' : <><Play size={16} /> Start Scan</>}
                    </button>
                </form>

                {error && (
                    <div style={{ marginTop: '20px', padding: '12px', background: 'rgba(247, 118, 142, 0.1)', color: 'var(--danger-color)', borderRadius: '8px' }}>
                        Error: {error}
                    </div>
                )}
            </div>

            <ResultsDisplay data={results} loading={loading} />
        </ScannerLayout>
    );
};

export default NmapScanner;
