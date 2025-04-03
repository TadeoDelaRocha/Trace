export async function loginAnalyst(initials: string, isLead: boolean) {
    const response = await fetch('http://localhost:8000/api/analyst/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ initials, is_lead: isLead })
    });
  
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }
  
    return response.json();
  }
  