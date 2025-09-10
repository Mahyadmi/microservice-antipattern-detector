
package architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.*;

public class ArchitectureTest {
    public static void main(String[] args) {
        JavaClasses classes = new ClassFileImporter()
            .importPath(".");
            
        // Check for cycles
        ArchRule noCycles = slices()
            .matching("com.(*)..")
            .should().beFreeOfCycles();
            
        // Check for proper layering
        ArchRule properLayering = classes()
            .that().resideInAPackage("..controller..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..service..", "..dto..", "java..");
            
        try {
            noCycles.check(classes);
        } catch (AssertionError e) {
            System.out.println("CYCLE_DETECTED: " + e.getMessage());
        }
        
        try {
            properLayering.check(classes);
        } catch (AssertionError e) {
            System.out.println("LAYER_VIOLATION: " + e.getMessage());
        }
    }
}
