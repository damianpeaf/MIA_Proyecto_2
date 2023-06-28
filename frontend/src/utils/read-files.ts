export const readFile = async (files: FileList): Promise<string[]> => {
    const promises = Array.from(files).map((file) => {
        return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (event) => {
                resolve(event.target?.result as string);
            };
            reader.onerror = (error) => {
                reject(error);
            };
            reader.readAsText(file);
        });
    });
    return Promise.all(promises);
}