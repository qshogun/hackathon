using System;
using System.IO;
using TechTalk.SpecFlow;
using TechTalk.SpecFlow.Configuration;

class Program
{
    static void Main(string[] args)
    {
        // Provide the path to your feature files directory
        string featureFilesDirectory = @"path\to\your\feature\files\directory";

        // Create a new SpecFlow runtime configuration
        var configuration = ConfigurationLoader.GetDefault();

        // Create a new SpecFlow runtime with the provided configuration
        var runtime = new TechTalk.SpecFlow.Runtime.Runtime(configuration);

        // Register the step definitions assembly with the runtime
        runtime.RegisterStepDefinitionSkeletonDiscoverer(new NullStepDefinitionSkeletonDiscoverer());
        runtime.RegisterDependencies((containerBuilder) =>
        {
            containerBuilder.RegisterTypeAssembliesFromPath(AppDomain.CurrentDomain.BaseDirectory);
        });

        // Create a new SpecFlow feature file parser
        var parser = new TechTalk.SpecFlow.Parser.Parser();

        // Get all feature files in the directory
        string[] featureFiles = Directory.GetFiles(featureFilesDirectory, "*.feature", SearchOption.AllDirectories);

        foreach (var featureFile in featureFiles)
        {
            Console.WriteLine($"Checking feature file: {featureFile}");

            // Parse the feature file
            var feature = parser.ParseFile(featureFile);

            // Initialize SpecFlow context
            var context = new SpecFlowExecutionContext(new SpecFlowConfigurationHolder(configuration), featureFile);

            foreach (var scenario in feature.Scenarios)
            {
                foreach (var step in scenario.Steps)
                {
                    // Try to match step to a step definition
                    var matchingStepDefinition = runtime.GetBindingMatch(step, context);

                    if (matchingStepDefinition == null)
                    {
                        Console.WriteLine($"Step '{step.Keyword}: {step.Text}' in scenario '{scenario.Title}' is not implemented.");
                    }
                }
            }

            Console.WriteLine();
        }
    }
}
