// @ts-check

import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default defineConfig([
    {
        files: ["**/*.{js,jsx,ts,tsx}"],

        extends: [
            js.configs.recommended,
            tseslint.configs.recommended,
            tseslint.configs.stylistic,
            reactHooks.configs.flat.recommended,
            reactRefresh.configs.vite,
        ],

        ignores: [
            "dist/**",
            "node_modules/**",
        ],
    },
]);