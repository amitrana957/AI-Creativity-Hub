import * as Yup from "yup";

type ValidationSchema = Yup.ObjectSchema<any>;

/**
 * validateInput
 * @param schema - Yup validation schema
 * @param data - object to validate
 * @returns {Promise<{ valid: boolean; error?: string }>}
 *          valid: true if valid, false if invalid
 *          error: validation error message if invalid
 */
export const validateInput = async (
  schema: ValidationSchema,
  data: object
): Promise<{ valid: boolean; error?: string }> => {
  try {
    await schema.validate(data);
    return { valid: true };
  } catch (error: any) {
    if (error.name === "ValidationError") {
      return { valid: false, error: error.message };
    }
    console.error("Validation Helper Error:", error);
    return { valid: false, error: "Unexpected validation error" };
  }
};

/**
 * createSchema
 * Utility to create a simple Yup string schema for required fields
 * @param fieldName - name of the field
 * @param requiredMessage - message for required validation
 */
export const createSchema = (fieldName: string, requiredMessage = "Input is required") =>
  Yup.object().shape({
    [fieldName]: Yup.string().required(requiredMessage).min(1, requiredMessage),
  });
