<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import {
		activeTab,
		name,
		date,
		time,
		owner,
		description,
		selectedProject,
		showCreateModal,
		openCreateModal,
		closeCreateModal,
		showEditModal,
		openEditModal,
		closeEditModal,
		submitEditForm,
		submitCreateForm,
		submitDeleteForm,
		submitLockForm,
		submitUnlockForm,
		openMenuFor,
		toggleMenu,
	} from './myProjectsLogic';

	export let data;
	let projects = data.projects;

	// Retrieve the logged-in user from local storage
	let loggedInUser: { initials: string; role: string } | null = null;
	onMount(() => {
		const storedUser = localStorage.getItem('user');
		if (storedUser) {
			loggedInUser = JSON.parse(storedUser);
		}
	});

	// Log out function: clear storage and redirect to home page
	function logout() {
		localStorage.removeItem('user');
		goto('/');
	}

	console.log('myProjects:', projects);
</script>

<div class="page-wrapper">
	<!-- User header with log out button -->
	<header class="user-header">
		{#if loggedInUser}
			<div class="user-info">
				<p>Logged in as: {loggedInUser.initials} ({loggedInUser.role})</p>
			</div>
			<button class="logout-btn" on:click={logout}>Log Out</button>
		{:else}
			<p>Not logged in</p>
		{/if}
	</header>

	<div class="top-bar">
		<h1>Project Selection</h1>
		<button class="create-btn" on:click={openCreateModal}>+ Create new</button>
	</div>

	<section class="recent-projects">
		<h2>Recent Projects</h2>
		<div class="recent-list">
			<div class="recent-card">Base Perimeter Network<br /><small>Nov 2, 2024</small></div>
			<div class="recent-card">Mission Control Portal<br /><small>Nov 1, 2024</small></div>
			<div class="recent-card">Field Operations<br /><small>Oct 31, 2024</small></div>
			<div class="recent-card">Government Defense<br /><small>Oct 30, 2024</small></div>
		</div>
	</section>

	<section class="all-projects">
		<h2>All Projects</h2>
		<div class="tabs">
			<button on:click={() => activeTab.set("my")} class:active={$activeTab === "my"}>My Projects</button>
			<button on:click={() => activeTab.set("shared")} class:active={$activeTab === "shared"}>Shared Projects</button>
		</div>

		<div class="table-wrapper">
			<table class="w-full h-full table-auto border">
				<thead>
					<tr>
						<th>Project Name</th>
						<th>Last Edit</th>
						<th>Lead Analyst</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each projects as project}
						<tr>
							<td>{project.name}</td>
							<td>{new Date(project.editTime).toLocaleDateString()}</td>
							<td>{project.owner}</td>
							<td>Run Scan</td>
							<td class="actions-cell">
								<div class="menu-wrapper">
									<button class="dots-btn" on:click={(e) => toggleMenu(project.name, e)}>⋯</button>

									{#if $openMenuFor === project.name}
										<!-- svelte-ignore a11y_click_events_have_key_events -->
										<!-- svelte-ignore a11y_no_static_element_interactions -->
										<div class="dropdown-menu" on:click|stopPropagation>
											{#if project.locked}
												<button on:click={() => {submitUnlockForm(project.name);}}>Unlock</button>
											{:else}
												<button on:click={() => {submitLockForm(project.name);}}>Lock</button>
												<button on:click={() => {submitDeleteForm(project.name);}}>Delete</button>
												<button on:click={() => {openEditModal(project);}}>Edit</button>
											{/if}
										</div>
									{/if}
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</section>
</div>

{#if $showEditModal}
	<div
	class="modal-overlay"
	on:click={closeEditModal}
	on:keydown={(e) => e.key === 'Enter' && closeEditModal()}
	tabindex="0"
	role="button"
	aria-label="Close modal"
	>
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="modal" on:click|stopPropagation>
		<div class="modal-header">
			<h2>Edit Project: {$selectedProject?.name}</h2>
			<button class="close-btn" on:click={closeEditModal}>×</button>
		</div>

		<form on:submit={submitEditForm}>
			<div class="form-grid">
				<label>
					Project Name *
					<input required bind:value={$name} />
				</label>
		
				<label>
					Start Date *
					<input type="date" required bind:value={$date} />
				</label>
		
				<label>
					Time *
					<input type="time" required bind:value={$time} />
				</label>
		
				<label>
					Lead Analyst Initials *
					<input required bind:value={$owner} />
				</label>
		
				<label class="description-field" style="grid-column: span 2;">
					Project Description
					<textarea rows="3" bind:value={$description}></textarea>
				</label>
			</div>
		
			<div class="modal-actions">
				<button type="button" class="cancel-btn" on:click={closeEditModal}>Cancel</button>
				<button type="submit" class="submit-btn">Save Changes</button>
			</div>
		</form>		
	</div>
	</div>
{/if}

{#if $showCreateModal}
	<div
		class="modal-overlay"
		on:click={closeCreateModal}
		on:keydown={(e) => e.key === 'Enter' && closeCreateModal()}
		tabindex="0"
		role="button"
		aria-label="Close modal"
	>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="modal" on:click|stopPropagation>
			<div class="modal-header">
				<h2>Create Project</h2>
				<button class="close-btn" on:click={closeCreateModal}>×</button>
			</div>

			<form on:submit={submitCreateForm}>
				<div class="form-grid">
					<label>
						Project Name *
						<input required bind:value={$name} />
					</label>

					<label>
						Start Date *
						<input type="date" required bind:value={$date} />
					</label>

					<label>
						Time *
						<input type="time" required bind:value={$time} />
					</label>

					<label>
						Lead Analyst Initials *
						<input required bind:value={$owner} />
					</label>

					<label class="description-field" style="grid-column: span 2;">
						Project Description
						<textarea rows="3" bind:value={$description}></textarea>
					</label>

					<label style="grid-column: span 2;">
						Upload NMap
						<input type="file" multiple />
					</label>
				</div>

				<div class="modal-actions">
					<button type="button" class="cancel-btn" on:click={closeCreateModal}>Cancel</button>
					<button type="submit" class="submit-btn">Create</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<style>
	.user-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		background-color: #f4f4f4;
		border-bottom: 1px solid #ccc;
	}
	.user-header .logout-btn {
		background: none;
		border: none;
		font-size: 0.9rem;
		cursor: pointer;
		color: #0070f3;
	}
	.page-wrapper {
		padding: 1rem;
	}
	.top-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 1rem;
	}
	/* Other styles remain as needed */
</style>
