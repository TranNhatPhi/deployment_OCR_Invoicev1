package com.project.myapp.Services;

import com.project.myapp.DTO.CategoryDTO;
import com.project.myapp.Model.Category;

import java.util.List;

public interface ICategoryService {
    Category getCategoryById(long id);
    Category CreateCategory(CategoryDTO category);

    List<Category> getAllCategories();
    Category UpdateCategory(long categoryId, CategoryDTO category);

    void deleteCategoryById(long id);
}
