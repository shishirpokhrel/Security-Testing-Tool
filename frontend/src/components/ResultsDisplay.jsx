import { Terminal, Copy, Check } from 'lucide-react';
import { useState } from 'react';

const ResultsDisplay = ({ data, title = "Scan Results", loading = false }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(JSON.stringify(data, null, 2));
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (!data && !loading) return null;

    return (
        <div className="card fade-in" style={{ marginTop: '24px', position: 'relative', overflow: 'hidden' }}>
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '16px',
                borderBottom: '1px solid var(--border-color)',
                paddingBottom: '12px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Terminal size={18} color="var(--primary-color)" />
                    <h3 style={{ margin: 0, fontSize: '16px' }}>{title}</h3>
                </div>

                {data && (
                    <button
                        onClick={handleCopy}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: copied ? 'var(--primary-color)' : 'var(--text-secondary)',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            fontSize: '12px'
                        }}
                    >
                        {copied ? <Check size={14} /> : <Copy size={14} />}
                        {copied ? 'Copied' : 'Copy JSON'}
                    </button>
                )}
            </div>

            <div style={{
                background: '#0d0e12',
                borderRadius: '8px',
                padding: '16px',
                fontFamily: 'monospace',
                fontSize: '13px',
                maxHeight: '500px',
                overflow: 'auto',
                color: '#a9b1d6',
                whiteSpace: 'pre-wrap'
            }}>
                {loading ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary-color)' }}>
                        <span className="spinner"></span> Scanning in progress...
                    </div>
                ) : (
                    JSON.stringify(data, null, 2)
                )}
            </div>
        </div>
    );
};

export default ResultsDisplay;
