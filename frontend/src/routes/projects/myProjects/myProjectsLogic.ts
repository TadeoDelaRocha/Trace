import { get, writable } from 'svelte/store';

export const activeTab = writable('my');
export const name = writable('');
export const date = writable('');
export const time = writable('');
export const owner = writable('');
export const description = writable('');
export const id = writable('');
export const showCreateModal = writable(false);
export const showEditModal = writable(false);

export const selectedProject = writable(null); 
export const openMenuFor = writable<string | null>(null);
export const menuPosition = writable({ top: 0, left: 0 });

export function openEditModal(project) {
	selectedProject.set(project);
	name.set(project.name);
	date.set(project.date?.split('T')[0]); // assumes ISO format
	time.set(project.date?.split('T')[1]?.slice(0, 5)); // hh:mm
	owner.set(project.owner);
	description.set(project.description || '');
	showEditModal.set(true);
}

export function closeEditModal() {
	showEditModal.set(false);
}

export function openCreateModal() {
	showCreateModal.set(true);
}

export function closeCreateModal() {
	showCreateModal.set(false);
}

export async function submitEditForm(event) {
	event.preventDefault();

	let $name = '', $date = '', $time = '', $owner = '', $description = '', $id = '';
	name.subscribe((v) => ($name = v))();
	date.subscribe((v) => ($date = v))();
	time.subscribe((v) => ($time = v))();
	owner.subscribe((v) => ($owner = v))();
	description.subscribe((v) => ($description = v))();
	id.subscribe((v) => ($id = v))();
	const original = get(selectedProject);

	const payload = {
		name: get(name),
		date: get(date),
		time: get(time),
		owner: get(owner),
		description: get(description),
		id: original?.id
	};
	
	try {
		const res = await fetch(`/api/projects/update`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		})
		
		closeEditModal();
		
		if (!res.ok) {
			const error = await res.text();
			console.error('Failed to update project:', error);
			alert('Error updating project');
			return;
		}

		const data = await res.json();
		console.log('Project updated:', data);
		alert('Project updated successfully!');
		showCreateModal.set(false);
	} catch (err) {
		console.error('Error:', err);
		alert('Something went wrong.');
	}
}


export async function submitDeleteForm(toDelete: string) {
    const payload = {
        toEdit: toDelete
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

export async function submitLockForm(toLock: string) {
    const payload = {
        toEdit: toLock
    };

    try {
        const res = await fetch('/api/projects/lock', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!res.ok) {
            const error = await res.text();
			console.error('Failed to lock project:', error);
			alert('Error locking project');
			return;
        }

        const data = await res.json();
		console.log('Project locked:', data);
		alert('Project locked successfully!');
		showCreateModal.set(false);
    } catch (err) {
		console.error('Error:', err);
		alert('Something went wrong.');
	}
}

export async function submitUnlockForm(toUnlock: string) {
    const payload = {
        toEdit: toUnlock
    };

    try {
        const res = await fetch('/api/projects/unlock', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!res.ok) {
            const error = await res.text();
			console.error('Failed to unlock project:', error);
			alert('Error unlocking project');
			return;
        }

        const data = await res.json();
		console.log('Project unlocked:', data);
		alert('Project unlocked successfully!');
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