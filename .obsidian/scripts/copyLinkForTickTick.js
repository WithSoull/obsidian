module.exports = async (params) => {
    const { app } = params;
    const activeFile = app.workspace.getActiveFile();

    if (!activeFile) {
        new Notice("Нет активной заметки.");
        return;
    }

    const noteTitle = activeFile.basename;
    const obsidianURL = `obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(activeFile.path)}`;
    
    const markdownLink = `[${noteTitle}](${obsidianURL})`;

    await navigator.clipboard.writeText(markdownLink);
    new Notice("Ссылка на заметку скопирована!");
};
