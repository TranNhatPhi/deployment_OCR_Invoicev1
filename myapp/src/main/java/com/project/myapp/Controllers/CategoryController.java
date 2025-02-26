package com.project.myapp.Controllers;

import com.project.myapp.DTO.CategoryDTO;
import com.project.myapp.Model.Category;
import com.project.myapp.Services.ICategoryService;
import jakarta.validation.Valid;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.HashSet;
import java.util.List;

@RestController
@RequestMapping("${api.prefix}/categories")
@RequiredArgsConstructor
@FieldDefaults(makeFinal=true,level = AccessLevel.PRIVATE)
public class CategoryController {
    ICategoryService categoryService;
    @GetMapping("")
    public ResponseEntity<?> GetAllCategory(@RequestParam("page") int page
            , @RequestParam("limit") int limit) {

            List<Category> categories = categoryService.getAllCategories();
            return ResponseEntity.ok(categories);
    }

    @PostMapping("")
    public ResponseEntity<?> CreateCategory(@Valid @RequestBody CategoryDTO categoryDTO,
                                            BindingResult result) {
        try{
        if (result.hasErrors()) {
        HashSet<String> errorMessages = new HashSet<>();
            result.getFieldErrors()
                    .forEach(error -> errorMessages.add(error.getDefaultMessage()));
            return ResponseEntity.badRequest().body(errorMessages);
        }
           Category categories= categoryService.CreateCategory(categoryDTO);
            return ResponseEntity.ok(categories);
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateCategory(@PathVariable Long id,
                                      @Valid @RequestBody  CategoryDTO categoryDTO
                                     ,BindingResult result) {
        try{
            if (result.hasErrors()) {
                HashSet<String> errorMessages = new HashSet<>();
                result.getFieldErrors()
                        .forEach(error -> errorMessages.add(error.getDefaultMessage()));
                return ResponseEntity.badRequest().body(errorMessages);
            }
            Category categoryUpdate = categoryService.UpdateCategory(id, categoryDTO);
            return ResponseEntity.ok(categoryUpdate);
        }catch (Exception ex){
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> DeleteCategory(@PathVariable Long id) {

           try {
               if(categoryService.getCategoryById(id) == null) {
                   return ResponseEntity.badRequest().body("not found id category:"+id);
               }
               categoryService.deleteCategoryById(id);
               return ResponseEntity.ok("delete category successfully");
           }catch (Exception ex){
               return ResponseEntity.badRequest().body(ex.getMessage());
           }
    }

}   
