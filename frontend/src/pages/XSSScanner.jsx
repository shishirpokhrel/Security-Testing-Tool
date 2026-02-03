import { useState } from 'react';
import axios from 'axios';
import ScannerLayout from '../components/ScannerLayout';
import ResultsDisplay from '../components/ResultsDisplay';
import { Play } from 'lucide-react';

const XSSScanner = () => {
    const [url, setUrl] = useState('');
    const [maxPayloads, setMaxPayloads] = useState(50);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleScan = async (e) => {
        e.preventDefault();
        if (!url) return;

        setLoading(true);
        setResults(null);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/api/scan/xss', {
                url,
                max_payloads: parseInt(maxPayloads)
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
            title="XSS Vulnerability Scanner"
            description="Detect Cross-Site Scripting vulnerabilities by injecting standard payloads into URL parameters and forms."
            badge="Web"
        >
            <div className="card" style={{ maxWidth: '800px' }}>
                <form onSubmit={handleScan} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Target URL</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g., http://example.com/search?q=test"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Max Payloads</label>
                        <input
                            type="number"
                            className="input"
                            value={maxPayloads}
                            onChange={(e) => setMaxPayloads(e.target.value)}
                            min="1"
                            max="1000"
                        />
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

            <ResultsDisplay data={results} loading={loading} title="Vulnerability Report" />
        </ScannerLayout>
    );
};

export default XSSScanner;
