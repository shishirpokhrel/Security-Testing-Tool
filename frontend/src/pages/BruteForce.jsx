import { useState } from 'react';
import axios from 'axios';
import ScannerLayout from '../components/ScannerLayout';
import ResultsDisplay from '../components/ResultsDisplay';
import { Play } from 'lucide-react';

const BruteForce = () => {
    const [target, setTarget] = useState('');
    const [protocol, setProtocol] = useState('http-basic');
    const [usernameField, setUsernameField] = useState('');
    const [passwordField, setPasswordField] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleScan = async (e) => {
        e.preventDefault();
        if (!target) return;

        setLoading(true);
        setResults(null);
        setError(null);

        const payload = {
            target,
            protocol,
            ...(protocol === 'http-form' && { username_field: usernameField, password_field: passwordField })
        };

        try {
            const response = await axios.post('http://localhost:8000/api/scan/bruteforce', payload);
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScannerLayout
            title="Brute Force Module"
            description="Test credentials against various protocols (HTTP, SSH, FTP) using wordlists."
            badge="Attack"
        >
            <div className="card" style={{ maxWidth: '800px' }}>
                <form onSubmit={handleScan} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Target</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g., http://example.com/login"
                            value={target}
                            onChange={(e) => setTarget(e.target.value)}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Protocol</label>
                        <select
                            className="input"
                            value={protocol}
                            onChange={(e) => setProtocol(e.target.value)}
                        >
                            <option value="http-basic">HTTP Basic Auth</option>
                            <option value="http-form">HTTP Form Post</option>
                            <option value="ssh">SSH</option>
                            <option value="ftp">FTP</option>
                        </select>
                    </div>

                    {protocol === 'http-form' && (
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Username Field</label>
                                <input
                                    type="text"
                                    className="input"
                                    placeholder="name='username'"
                                    value={usernameField}
                                    onChange={(e) => setUsernameField(e.target.value)}
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Password Field</label>
                                <input
                                    type="text"
                                    className="input"
                                    placeholder="name='password'"
                                    value={passwordField}
                                    onChange={(e) => setPasswordField(e.target.value)}
                                />
                            </div>
                        </div>
                    )}

                    <div style={{ padding: '12px', background: 'rgba(224, 175, 104, 0.1)', borderRadius: '8px' }}>
                        <p style={{ margin: 0, fontSize: '12px', color: 'var(--warning-color)' }}>
                            Note: Uses default wordlists on the server. Ensure you have permission to test this target.
                        </p>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ alignSelf: 'flex-start' }}
                        disabled={loading}
                    >
                        {loading ? 'Attacking...' : <><Play size={16} /> Start Attack</>}
                    </button>
                </form>

                {error && (
                    <div style={{ marginTop: '20px', padding: '12px', background: 'rgba(247, 118, 142, 0.1)', color: 'var(--danger-color)', borderRadius: '8px' }}>
                        Error: {error}
                    </div>
                )}
            </div>

            <ResultsDisplay data={results} loading={loading} title="Attempt Results" />
        </ScannerLayout>
    );
};

export default BruteForce;
