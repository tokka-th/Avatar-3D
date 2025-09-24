// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Misc/Paths.h"
#include "HAL/PlatformProcess.h"
#include "MyBlueprintFunctionLibrary.generated.h"

/**
 * 
 */
UCLASS()
class AVATARCPP7_API UMyBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category = "System")
	static void RunBatchFile(const FString& FilePath)
	{
		if (!FilePath.IsEmpty())
		{
			UE_LOG(LogTemp, Error, TEXT("Running batch file : % s"), *FilePath);
			UE_LOG(LogTemp, Error, TEXT("FPlatformProcess::CreateProc(*FilePath, nullptr, true, true, true, nullptr, 0, nullptr, nullptr, 0);"));
			FPlatformProcess::CreateProc(*FilePath, nullptr, true, false, false, nullptr, 0, nullptr, nullptr);
			//FPlatformProcess::ExecProcess(*(FilePath), nullptr, false, false, false);
		}
		else
		{
			UE_LOG(LogTemp, Error, TEXT("Can't open"));
		}

	}

	UFUNCTION(BlueprintCallable, Category = "System")
	static FString ResolvePath(const FString& RelativePath)
	{

		// Base directory = where your packaged .exe is located
		/*FString BaseDir = FPlatformProcess::BaseDir();

		// Combine base dir with your relative path
		FString CombinedPath = FPaths::ConvertRelativePathToFull(FPaths::Combine(BaseDir, RelativePath));

		// Log it for debugging
		UE_LOG(LogTemp, Warning, TEXT("BaseDir: %s"), *BaseDir);
		UE_LOG(LogTemp, Warning, TEXT("RelativePath: %s"), *RelativePath);
		UE_LOG(LogTemp, Warning, TEXT("Resolved Absolute Path: %s"), *CombinedPath);

		return CombinedPath;*/

		FString FinalPath;

		// Check if path is already absolute
		if (FPaths::IsRelative(RelativePath))
		{
			// Base directory = where packaged .exe lives
			FString BaseDir = FPlatformProcess::BaseDir();

			// Combine and normalize
			FinalPath = FPaths::ConvertRelativePathToFull(FPaths::Combine(BaseDir, RelativePath));

			UE_LOG(LogTemp, Warning, TEXT("[ResolvePath] Relative → Absolute"));
		}
		else
		{
			// Already absolute, just normalize
			FinalPath = FPaths::ConvertRelativePathToFull(RelativePath);

			UE_LOG(LogTemp, Warning, TEXT("[ResolvePath] Already Absolute"));
		}

		// Log for debugging
		UE_LOG(LogTemp, Warning, TEXT("Input Path: %s"), *RelativePath);
		UE_LOG(LogTemp, Warning, TEXT("Resolved Path: %s"), *FinalPath);

		return FinalPath;
	}




	
};
