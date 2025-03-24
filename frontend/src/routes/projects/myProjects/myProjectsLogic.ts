import { writable } from 'svelte/store';

export const activeTab = writable('my');
export const name = writable('');
export const date = writable('');
export const time = writable('');
export const owner = writable('');
export const description = writable('');
export const showCreateModal = writable(false);

export const openMenuFor = writable<string | null>(null);
export const menuPosition = writable({ top: 0, left: 0 });

export function openCreateModal() {
	showCreateModal.set(true);
}

export function closeCreateModal() {
	showCreateModal.set(false);
}

export async function submitDeleteForm(toDelete: string) {
    const payload = {
        toDelete: toDelete
    };

    try {
        const res = await fetch('/api/projects/delete', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!res.ok) {
            const error = await res.text();
			console.error('Failed to delete project:', error);
			alert('Error deleting project');
			return;
        }

        const data = await res.json();
		console.log('Project deleted:', data);
		alert('Project deleted successfully!');
		showCreateModal.set(false);
    } catch (err) {
		console.error('Error:', err);
		alert('Something went wrong.');
	}
}

export async function submitCreateForm(event: Event) {
	event.preventDefault();

	let $name = '', $date = '', $time = '', $owner = '', $description = '';
	name.subscribe((v) => ($name = v))();
	date.subscribe((v) => ($date = v))();
	time.subscribe((v) => ($time = v))();
	owner.subscribe((v) => ($owner = v))();
	description.subscribe((v) => ($description = v))();

	const payload = {
		name: $name,
		date: $date,
		time: $time,
		owner: $owner,
		description: $description
	};

	try {
		const res = await fetch('/api/projects/create', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (!res.ok) {
			const error = await res.text();
			console.error('Failed to create project:', error);
			alert('Error creating project');
			return;
		}

		const data = await res.json();
		console.log('Project created:', data);
		alert('Project created successfully!');
		showCreateModal.set(false);
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