import { writable } from 'svelte/store';

export const openMenuFor = writable<string | null>(null);
export const menuPosition = writable({ top: 0, left: 0 });

export async function submitRestoreForm(toRestore: string) {
    const payload = {
        toEdit: toRestore
    };

    console.log("Submitting banish request:", payload);

    try {
        const res = await fetch('/api/projects/restore', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!res.ok) {
            const error = await res.text();
            console.error('Failed to restore project:', error);
            alert('Error restoring project');
            return;
        }

        const data = await res.json();
        console.log('Project restored:', data);
        alert('Project restored successfully!');
    } catch (err) {
        console.error('Error:', err);
        alert('Something went wrong.');
    }
}

export async function submitBanishForm(toBanish: string) {
    const payload = {
        toEdit: toBanish
    };

    console.log("Submitting banish request:", payload);

    try {
        const res = await fetch('/api/projects/banish', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!res.ok) {
            const error = await res.text();
            console.error('Failed to banish project:', error);
            alert('Error banishing project');
            return;
        }

        const data = await res.json();
        console.log('Project banished:', data);
        alert('Project banished successfully!');
    } catch (err) {
        console.error('Error:', err);
        alert('Something went wrong.');
    }
}

export function toggleMenu(projectName: string, event: MouseEvent) {
    const rect = (event.target as HTMLElement).getBoundingClientRect();
    menuPosition.set({
        top: rect.bottom + window.scrollY,
        left: rect.left + window.scrollX
    });

    openMenuFor.update((current) => (current === projectName ? null : projectName));
}

export function closeMenu() {
    openMenuFor.set(null);
}