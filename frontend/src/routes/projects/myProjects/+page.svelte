<script lang="ts">
	import { page } from '$app/stores';
	import './myProjects.css';
	import {
		activeTab,
		name,
		date,
		time,
		owner,
		description,
		showCreateModal,
		openCreateModal,
		closeCreateModal,
		submitCreateForm,
        submitDeleteForm,
		openMenuFor,
		menuPosition,
		toggleMenu,
		closeMenu
	} from './myProjectsLogic';

	export let data;
	let projects = data.projects;

	console.log('myProjects:', projects);
</script>

<div class="page-wrapper">
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
											<button on:click={() => console.log('Lock', project.name)}>Lock</button>
											<button on:click={() => {submitDeleteForm(project.name);}}
                                        >
                                            Delete
                                        </button>
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
