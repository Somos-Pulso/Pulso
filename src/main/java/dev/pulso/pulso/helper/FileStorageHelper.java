package dev.pulso.pulso.helper;

import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Component
public class FileStorageHelper {

    private final String baseUploadDir = "uploads/";

    public String saveFile(MultipartFile file, String folder, String prefix) throws IOException {
        Path uploadPath = Paths.get(baseUploadDir, folder);
        Files.createDirectories(uploadPath);

        String filename = prefix + "_" + file.getOriginalFilename();
        Path filepath = uploadPath.resolve(filename);
        file.transferTo(filepath.toFile());

        return folder + "/" + filename;
    }
}
