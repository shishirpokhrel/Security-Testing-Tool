import { useState } from 'react';
import axios from 'axios';
import ScannerLayout from '../components/ScannerLayout';
import ResultsDisplay from '../components/ResultsDisplay';
import { Play } from 'lucide-react';

const SubfinderScanner = () => {
    const [domain, setDomain] = useState('');
    const [sources, setSources] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleScan = async (e) => {
        e.preventDefault();
        if (!domain) return;

        setLoading(true);
        setResults(null);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/api/scan/subfinder', {
                domain,
                sources: sources || undefined
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
            title="Subfinder Enumeration"
            description="Passive subdomain enumeration tool that discovers valid subdomains for websites."
            badge="Recon"
        >
            <div className="card" style={{ maxWidth: '800px' }}>
                <form onSubmit={handleScan} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Target Domain</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g., example.com"
                            value={domain}
                            onChange={(e) => setDomain(e.target.value)}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Sources (Optional)</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g., virustotal,shodan (comma separated)"
                            value={sources}
                            onChange={(e) => setSources(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ alignSelf: 'flex-start' }}
                        disabled={loading}
                    >
                        {loading ? 'Enumerating...' : <><Play size={16} /> Start Scan</>}
                    </button>
                </form>

                {error && (
                    <div style={{ marginTop: '20px', padding: '12px', background: 'rgba(247, 118, 142, 0.1)', color: 'var(--danger-color)', borderRadius: '8px' }}>
                        Error: {error}
                    </div>
                )}
            </div>

            <ResultsDisplay data={results} loading={loading} title="Discovered Subdomains" />
        </ScannerLayout>
    );
};

export default SubfinderScanner;
