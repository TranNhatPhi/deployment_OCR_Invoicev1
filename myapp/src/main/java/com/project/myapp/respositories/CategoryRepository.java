package com.project.myapp.respositories;

import com.project.myapp.Model.Category;
import org.springframework.data.jpa.repository.JpaRepository;


public interface CategoryRepository extends JpaRepository<Category,Long> {


}
