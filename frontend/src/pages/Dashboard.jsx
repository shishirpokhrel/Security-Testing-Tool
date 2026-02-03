import { Shield, Activity, Lock, Globe } from 'lucide-react';

const CreateStatCard = ({ icon: Icon, label, value, color }) => (
    <div className="card fade-in" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{
            padding: '12px',
            borderRadius: '12px',
            background: `rgba(${color}, 0.1)`,
            color: `rgb(${color})`
        }}>
            <Icon size={24} />
        </div>
        <div>
            <h3 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>{value}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '14px' }}>{label}</p>
        </div>
    </div>
);

const Dashboard = () => {
    return (
        <div>
            <header style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', marginBottom: '8px' }}>Dashboard</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Welcome back, Operator. System ready.</p>
            </header>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                gap: '24px',
                marginBottom: '32px'
            }}>
                <CreateStatCard icon={Shield} label="Total Scans" value="24" color="0, 255, 148" />
                <CreateStatCard icon={Activity} label="Active Tasks" value="0" color="122, 162, 247" />
                <CreateStatCard icon={Lock} label="Vulns Found" value="12" color="247, 118, 142" />
                <CreateStatCard icon={Globe} label="Targets Map" value="5" color="224, 175, 104" />
            </div>

            <div className="card fade-in">
                <h2 style={{ fontSize: '20px', marginBottom: '20px' }}>Recent Activity</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {[1, 2, 3].map((i) => (
                        <div key={i} style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            paddingBottom: '16px',
                            borderBottom: i < 3 ? '1px solid var(--border-color)' : 'none'
                        }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--primary-color)' }}></div>
                                <div>
                                    <p style={{ margin: 0, fontWeight: '500' }}>Nmap Scan Report</p>
                                    <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-secondary)' }}>Target: 192.168.1.{100 + i}</p>
                                </div>
                            </div>
                            <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>2 mins ago</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
