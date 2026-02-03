import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Radio, Search, ShieldAlert, Code2 } from 'lucide-react';

const Sidebar = () => {
    const navItems = [
        { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
        { path: '/nmap', icon: Radio, label: 'Nmap Scanner' },
        { path: '/subfinder', icon: Search, label: 'Subfinder' },
        { path: '/bruteforce', icon: ShieldAlert, label: 'Brute Force' },
        { path: '/xss', icon: Code2, label: 'XSS Scanner' },
    ];

    return (
        <aside style={{
            width: '260px',
            height: '100vh',
            background: 'var(--surface-color)',
            borderRight: '1px solid var(--border-color)',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <div style={{ marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                    width: '32px',
                    height: '32px',
                    background: 'var(--primary-color)',
                    borderRadius: '8px',
                    boxShadow: '0 0 15px var(--primary-glow)'
                }}></div>
                <h1 style={{ fontSize: '20px', fontWeight: 'bold', letterSpacing: '-0.5px' }}>SecTool</h1>
            </div>

            <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        style={({ isActive }) => ({
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            padding: '12px 16px',
                            borderRadius: 'var(--radius-md)',
                            textDecoration: 'none',
                            color: isActive ? '#fff' : 'var(--text-secondary)',
                            background: isActive ? 'rgba(0, 255, 148, 0.1)' : 'transparent',
                            border: isActive ? '1px solid rgba(0, 255, 148, 0.2)' : '1px solid transparent',
                            transition: 'all 0.2s ease'
                        })}
                    >
                        <item.icon size={20} />
                        <span style={{ fontSize: '14px', fontWeight: '500' }}>{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid var(--border-color)' }}>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                    Security Scanner v1.0<br />
                    &copy; 2026
                </p>
            </div>
        </aside>
    );
};

export default Sidebar;
